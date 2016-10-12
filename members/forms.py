from django.forms import Form, ModelForm, Textarea, CharField, EmailField, PasswordInput, BooleanField, FileField, ChoiceField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import ClearableFileInput, Select
from meetings.models import Report, Meeting
from .models import Student, Professor
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.core.validators import RegexValidator
from links.models import Dir
from multiupload.fields import MultiFileField
from django.forms.formsets import BaseFormSet


class ChangeFileReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ('file', )


class DirChangeForm(ModelForm):
    files = MultiFileField(min_num=1, max_num=15, max_file_size=1024 * 1024 * 50, required=False)

    class Meta:
        model = Dir
        fields = ('name', 'description', 'files')


class ReportChangeForm(ModelForm):
    author = ChoiceField(widget=Select, choices=((x.user, x.name_en()) for x in list(Professor.objects.all()) + list(Student.objects.all())))

    class Meta:
        model = Report
        fields = ('name', 'author', 'author_first_name_en', 'author_last_name_en', 'author_first_name_ua',
                  'author_last_name_ua', )
        labels = {
            'name': _('Report name'),
            'author': _('Author name'),
            'author_first_name_en': _('Author first name in En'),
            'author_last_name_en': _('Author last name in En'),
            'author_first_name_ua': _('Author first name in UA'),
            'author_last_name_ua': _('Author last name in Ua'),
        }

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if User.objects.filter(username=author).exists():
            author=User.objects.get(username=author)
        else:
            raise ValidationError(_('This author isn`t user'))
        return author


class MeetingChangeForm(ModelForm):

    class Meta:
        model = Meeting
        fields = ('topic_text', 'detail_text', 'meeting_date', )
        labels = {
            'topic_text': _('Topic of meeting'),
            'detail_text': _('Description of meeting (not required)'),
            'meeting_date': _('Date of meeting')
        }
        widgets = {
            'detail_text': Textarea(attrs={'cols': 70, 'rows': 3}),
            'meeting_date': SelectDateWidget(),
        }


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', _('Only alphanumeric characters are allowed.'))
alphabetic = RegexValidator(r'^[a-zA-Z]*$', _('Only alphabetic characters are allowed.'))


class StudentCreateForm(ModelForm):
    user_name = CharField(max_length=30, validators=[alphanumeric])
    email = EmailField(required=False)
    password = CharField(max_length=12, widget=PasswordInput, validators=[alphanumeric])

    class Meta:
        model = Student
        fields = ('user_name', 'password', 'email', 'first_name_en', 'last_name_en', 'first_name_ua', 'last_name_ua',
                  'course', 'group', 'institution', 'interests_en', 'interests_ua', 'photo', )
        widgets = {
            'password': PasswordInput(),
        }

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if User.objects.filter(username=user_name).exists():
            raise ValidationError(_('This user name is already in use.'))
        return user_name

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError(_('Password too short'))
        return password


class StudentEditForm(ModelForm):
    user_name = CharField(max_length=30, validators=[alphanumeric])
    email = EmailField(required=False)
    password = CharField(max_length=12, widget=PasswordInput, validators=[alphanumeric], required=False)

    class Meta:
        model = Student
        fields = ('user_name', 'password', 'email', 'first_name_en', 'last_name_en', 'first_name_ua', 'last_name_ua',
                  'course', 'group', 'institution', 'interests_en', 'interests_ua', 'photo', )
        widgets = {
            'password': PasswordInput,
            'photo': ClearableFileInput,
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 and password != r'':
            raise ValidationError(_('Password too short'))
        return password

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo.name[-3:] == r'gif':
            raise ValidationError(_('Gif files don`t allowed'))
        return photo


class ProfessorEditForm(ModelForm):
    user_name = CharField(max_length=30, validators=[alphanumeric])
    email = EmailField(required=False)
    password = CharField(max_length=12, widget=PasswordInput, validators=[alphanumeric], required=False)

    class Meta:
        model = Professor
        fields = ('user_name', 'password', 'email', 'first_name_en', 'last_name_en', 'first_name_ua', 'last_name_ua',
                  'academic_title', 'institution', 'position', 'interests_en', 'interests_ua', 'photo',)
        widgets = {
            'password': PasswordInput,
            'photo': ClearableFileInput,
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 and password != r'':
            raise ValidationError(_('Password too short'))
        return password

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo.name[-3:] == r'gif':
            raise ValidationError(_('Gif files don`t allowed'))
        return photo

