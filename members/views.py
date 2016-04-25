from django.views import generic
from django.utils import timezone
from .models import Student, Professor
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.decorators import method_decorator
from meetings.models import Report
from .forms import StudentForm


class IndexView(generic.TemplateView):
    template_name = 'members/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['professors'] = Professor.objects.all()
        context['students'] = Student.objects.filter(join_date__lte=timezone.now()).order_by('-join_date')[:10].reverse()
        return context


class DetailProfessorView(generic.DetailView):
    model = Professor
    template_name = 'members/detail_prof.html'


class DetailStudentView(generic.DetailView):
    model = Student
    template_name = 'members/detail_stud.html'


class LoggedInMixinStudent(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinStudent, self).dispatch(*args, **kwargs)


def not_in_student_group(user):
    if user:
        return user.groups.filter(name='Professors').exists()
    return False


class LoggedInMixinProfessor(object):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(not_in_student_group))
    def dispatch(self, *args, **kwargs):
        if not_in_student_group(self.user):
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        return super(LoggedInMixinStudent, self).dispatch(*args, **kwargs)


class ProfileProfessorView(LoggedInMixinProfessor, generic.TemplateView):
    template_name = 'members/professor_profile.html'


class ReportChangeView(LoggedInMixinStudent, generic.TemplateView):
    template_name = 'members/report_change.html'

    def get_context_data(self, **kwargs):
        context = super(ReportChangeView, self).get_context_data(**kwargs)
        context['form'] = StudentForm()
        context['reports'] = Report.objects.filter(author=self.request.user)
        return context


def send_report(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.file = request.FILES['file']
            report.author = request.user
            report.save()
            return redirect('meetings:detail', pk=report.meeting.pk)
    else:
        form = StudentForm()
    return render(request, 'members/report_change.html', {'form': form})


def edit_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.file = request.FILES['file']
            report.save()
            return HttpResponseRedirect(reverse('members:profile_view'))
    else:
        form = StudentForm(instance=report)
    return render(request, 'members/report_change.html', {'form': form})


@login_required
def profile_view(request):
    if request.user.groups.filter(name='Professors').exists():
        return HttpResponseRedirect(reverse('members:profile_professor_view'))
    elif request.user.groups.filter(name='Students').exists():
        return HttpResponseRedirect(reverse('members:report_change'))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

