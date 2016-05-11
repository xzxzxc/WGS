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
from links.models import Dir, File
from .forms import ReportChangeForm, MeetingChangeForm, StudentEditForm, StudentCreateForm, ProfessorEditForm,\
    DirChangeForm
from django.contrib.auth.models import User, Group


class IndexView(generic.TemplateView):
    template_name = 'members/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['professors'] = Professor.objects.all()
        context['students'] = Student.objects.filter(join_date__lte=timezone.now()).order_by('-join_date')[:15]
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


def in_professor_group(user):
    if user:
        return user.groups.filter(name='Professors').exists()
    return False


def in_professor_group_or_super(user):
    if user:
        if user.groups.filter(name='Professors').exists() or user.is_superuser:
            return True
    return False


def in_student_group(user):
    if user:
        return user.groups.filter(name='Students').exists()
    return False


class LoggedInMixinProfessor(object):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(in_professor_group))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinProfessor, self).dispatch(*args, **kwargs)


class LoggedInMixinProfessorOrSuper(object):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(in_professor_group_or_super))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinProfessorOrSuper, self).dispatch(*args, **kwargs)


class ProfileProfessorView(LoggedInMixinProfessor, generic.TemplateView):
    template_name = 'members/professor_profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileProfessorView, self).get_context_data(**kwargs)
        context['professor'] = Professor.objects.get(user=self.request.user)
        return context


class ProfileStudentView(LoggedInMixinStudent, generic.TemplateView):
    template_name = 'members/student_profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileStudentView, self).get_context_data(**kwargs)
        context['student'] = Student.objects.get(user=self.request.user)
        return context


class MeetingChangeView(LoggedInMixinProfessorOrSuper, generic.TemplateView):
    template_name = 'members/meeting_change.html'

    def get_context_data(self, **kwargs):
        context = super(MeetingChangeView, self).get_context_data(**kwargs)
        context['form'] = MeetingChangeForm
        context['meetings'] = Meeting.objects.all().order_by('-meeting_date')
        return context


@login_required
@user_passes_test(in_professor_group_or_super)
def send_meeting(request):
    if request.method == "POST":
        form = MeetingChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('members:meeting_change'))
    else:
        form = MeetingChangeForm()
    return render(request, 'members/meeting_change.html', {'form': form})


@login_required
@user_passes_test(in_professor_group_or_super)
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


@login_required
@user_passes_test(in_professor_group_or_super)
def delete_meeting(request, pk):
    get_object_or_404(Meeting, pk=pk).delete()
    return HttpResponseRedirect(reverse('members:meeting_change'))


class ReportChangeView(LoggedInMixinStudent, generic.TemplateView):
    template_name = 'members/report_change.html'

    def get_context_data(self, **kwargs):
        context = super(ReportChangeView, self).get_context_data(**kwargs)
        context['form'] = ReportChangeForm()
        context['reports'] = Report.objects.filter(author=self.request.user).order_by('-meeting')
        return context


@login_required
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
            return HttpResponseRedirect(reverse('members:report_change'))
    else:
        form = ReportChangeForm()
    return render(request, 'members/report_change.html', {'form': form})


@login_required
def edit_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportChangeForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
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
def delete_report(request, pk):
    get_object_or_404(Report, pk=pk).delete()
    return HttpResponseRedirect(reverse('members:report_change'))


class StudentChangeView(LoggedInMixinProfessor, generic.TemplateView):
    template_name = 'members/student_change.html'

    def get_context_data(self, **kwargs):
        context = super(StudentChangeView, self).get_context_data(**kwargs)
        context['form'] = StudentCreateForm
        context['students'] = Student.objects.all().order_by('-join_date')
        return context


@login_required
@user_passes_test(in_professor_group)
def send_student(request):
    if request.method == "POST":
        form = StudentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            # create and add new user to student
            new_user = User.objects.create_user(form.cleaned_data['user_name'], form.cleaned_data['email'],
                                                form.cleaned_data['password'])
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            students_group = Group.objects.get(name='Students')
            students_group.user_set.add(new_user)
            student.user = new_user
            # add photo
            try:
                student.photo = request.FILES['photo']
            except MultiValueDictKeyError:
                pass
            student.save()
            return HttpResponseRedirect(reverse('members:student_change'))
    else:
        form = StudentCreateForm()
    return render(request, 'members/student_change.html', {'form': form})


@login_required
@user_passes_test(in_professor_group)
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = student.user
    if request.method == "POST":
        form = StudentEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            user.username = form.cleaned_data['user_name']
            user.email = form.cleaned_data['email']
            new_password = form.cleaned_data['password']
            if new_password != r'':
                user.set_password(new_password)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            try:
                student.photo = request.FILES['photo']
            except MultiValueDictKeyError:
                pass
            student.save()
            return HttpResponseRedirect(reverse('members:student_change'))
    else:
        data = {
            'user_name': user.username,
            'password': r'',
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'course': student.course,
            'position': student.position,
        }
        form = StudentEditForm(data, instance=student)
    return render(request, 'members/student_change.html', {'form': form})


@login_required
@user_passes_test(in_professor_group)
def delete_student(request, pk):
    get_object_or_404(Student, pk=pk).user.delete()
    return HttpResponseRedirect(reverse('members:student_change'))


class DirChangeView(LoggedInMixinProfessor, generic.TemplateView):
    template_name = 'members/dir_change.html'

    def get_context_data(self, **kwargs):
        context = super(DirChangeView, self).get_context_data(**kwargs)
        context['form'] = DirChangeForm
        context['dirs'] = Dir.objects.all()
        return context


@login_required
@user_passes_test(in_professor_group)
def send_dir(request):
    if request.method == "POST":
        form = DirChangeForm(request.POST, request.FILES)
        if form.is_valid():
            dir = form.save(commit=False)
            dir.author = Professor.objects.get(user=request.user)
            dir.save()
            for each in form.cleaned_data['files']:
                File.objects.create(file=each, dir=dir)
            return HttpResponseRedirect(reverse('members:dir_change'))
    else:
        form = DirChangeForm()
    return render(request, 'members/dir_change.html', {'form': form})


@login_required
@user_passes_test(in_professor_group)
def edit_dir(request, pk):
    dir = get_object_or_404(Dir, pk=pk)
    if request.method == "POST":
        form = DirChangeForm(request.POST, request.FILES, instance=dir)
        if form.is_valid():
            dir = form.save(commit=False)
            for each in form.cleaned_data['files']:
                File.objects.create(file=each, dir=dir)
            dir.save()
            return HttpResponseRedirect(reverse('members:dir_change'))
    else:
        form = DirChangeForm(instance=dir)
        files = File.objects.filter(dir=dir)
    return render(request, 'members/dir_change.html', {'form': form, 'files': files, 'dir': dir})


@login_required
@user_passes_test(in_professor_group)
def delete_dir(request, pk):
    get_object_or_404(Dir, pk=pk).delete()
    return HttpResponseRedirect(reverse('members:dir_change'))


@login_required
@user_passes_test(in_professor_group)
def delete_file(request, dir_pk, file_pk):
    get_object_or_404(File, pk=file_pk).delete()
    return HttpResponseRedirect(reverse('members:edit_dir', kwargs={'pk': dir_pk}))


@login_required
@user_passes_test(in_professor_group)
def edit_professor_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    professor = Professor.objects.get(user=user)
    if request.method == "POST":
        form = ProfessorEditForm(request.POST, request.FILES, instance=professor)
        if form.is_valid():
            professor = form.save(commit=False)
            user.username = form.cleaned_data['user_name']
            user.email = form.cleaned_data['email']
            new_password = form.cleaned_data['password']
            if new_password != r'':
                user.set_password(new_password)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            try:
                professor.photo = request.FILES['photo']
            except MultiValueDictKeyError:
                pass
            professor.save()
            return redirect('members:professor_profile')
    else:
        data = {
            'user_name': user.username,
            'password': r'',
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'academic_title': professor.academic_title,
            'position': professor.position,
        }
        form = ProfessorEditForm(data, instance=professor)
    return render(request, 'members/professor_profile.html', {'form': form, 'professor': professor})


@login_required
@user_passes_test(in_student_group)
def edit_student_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    student = Student.objects.get(user=user)
    if request.method == "POST":
        form = StudentEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            user.username = form.cleaned_data['user_name']
            user.email = form.cleaned_data['email']
            new_password = form.cleaned_data['password']
            if new_password != r'':
                user.set_password(new_password)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            try:
                student.photo = request.FILES['photo']
            except MultiValueDictKeyError:
                pass
            student.save()
            return redirect('members:student_profile')
    else:
        data = {
            'user_name': user.username,
            'password': r'',
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'course': student.course,
            'position': student.position,
        }
        form = StudentEditForm(data, instance=student)
    return render(request, 'members/student_profile.html', {'form': form, 'student': student})


@login_required
def profile_view(request):
    if request.user.groups.filter(name='Professors').exists():
        return HttpResponseRedirect(reverse('members:professor_profile'))
    elif request.user.groups.filter(name='Students').exists():
        return HttpResponseRedirect(reverse('members:student_profile'))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
