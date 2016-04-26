from django.views import generic
from django.utils import timezone
from .models import Student, Professor
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError
from meetings.models import Report, Meeting
from .forms import ReportChangeForm, MeetingChangeForm


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


def not_in_professor_group(user):
    if user:
        return user.groups.filter(name='Professors').exists()
    return False


class LoggedInMixinProfessor(object):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(not_in_professor_group))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinProfessor, self).dispatch(*args, **kwargs)


class ProfileProfessorView(LoggedInMixinProfessor, generic.TemplateView):
    template_name = 'members/professor_profile.html'


class MeetingChangeView(LoggedInMixinProfessor, generic.TemplateView):
    template_name = 'members/meeting_change.html'

    def get_context_data(self, **kwargs):
        context = super(MeetingChangeView, self).get_context_data(**kwargs)
        context['form'] = MeetingChangeForm
        context['meetings'] = Meeting.objects.all().order_by('-meeting_date')
        return context


def send_meeting(request):
    if request.method == "POST":
        form = MeetingChangeForm(request.POST)
        if form.is_valid():
            meeting = form.save()
            return redirect('meetings:detail', pk=meeting.pk)
    else:
        form = MeetingChangeForm()
    return render(request, 'members/meeting_change.html', {'form': form})


def edit_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if request.method == "POST":
        form = MeetingChangeForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting.save()
            return HttpResponseRedirect(reverse('members:meeting_change'))
    else:
        form = MeetingChangeForm(instance=meeting)
    return render(request, 'members/meeting_change.html', {'form': form})


class ReportChangeView(LoggedInMixinStudent, generic.TemplateView):
    template_name = 'members/report_change.html'

    def get_context_data(self, **kwargs):
        context = super(ReportChangeView, self).get_context_data(**kwargs)
        context['form'] = ReportChangeForm()
        context['reports'] = Report.objects.filter(author=self.request.user).order_by('-meeting')
        return context


def send_report(request):
    if request.method == "POST":
        form = ReportChangeForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            try:
                report.file = request.FILES['file']
            except MultiValueDictKeyError:
                pass
            report.author = request.user
            report.save()
            return redirect('meetings:detail', pk=report.meeting.pk)
    else:
        form = ReportChangeForm()
    return render(request, 'members/report_change.html', {'form': form})


def edit_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportChangeForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            try:
                report.file = request.FILES['file']
            except MultiValueDictKeyError:
                pass
            report.save()
            return HttpResponseRedirect(reverse('members:report_change'))
    else:
        form = ReportChangeForm(instance=report)
    return render(request, 'members/report_change.html', {'form': form})


@login_required
def profile_view(request):
    if request.user.groups.filter(name='Professors').exists():
        return HttpResponseRedirect(reverse('members:profile_professor_view'))
    elif request.user.groups.filter(name='Students').exists():
        return HttpResponseRedirect(reverse('members:report_change'))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

