from django.forms import ModelForm, Textarea, CharField, EmailField, PasswordInput
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import ClearableFileInput
from meetings.models import Report, Meeting
from .models import Student, Professor
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.core.validators import RegexValidator
from links.models import Dir, File
from multiupload.fields import MultiFileField


class ReportChangeForm(ModelForm):

    class Meta:
        model = Report
        fields = ('meeting', 'name', 'file', )


class DirChangeForm(ModelForm):
    files = MultiFileField(min_num=1, max_num=15, max_file_size=1024 * 1024 * 50)

    class Meta:
        model = Dir
        fields = ('name', 'description', 'files')


class MeetingChangeForm(ModelForm):

    class Meta:
        model = Meeting
        fields = ('topic_text', 'detail_text', 'meeting_date', )
        labels = {
            'topic_text': _('Topic of meeting'),
            'detail_text': _('Description of meeting'),
            'meeting_date': _('Date of meeting')
        }
        widgets = {
            'detail_text': Textarea(attrs={'cols': 70, 'rows': 10}),
            'meeting_date': SelectDateWidget(),
        }

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
alphabetic = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')


class StudentCreateForm(ModelForm):
    user_name = CharField(max_length=30, validators=[alphanumeric])
    first_name = CharField(max_length=50, validators=[alphabetic])
    last_name = CharField(max_length=50, validators=[alphabetic])
    email = EmailField(required=False)
    password = CharField(max_length=12, widget=PasswordInput, validators=[alphanumeric])

    class Meta:
        model = Student
        fields = ('user_name', 'password', 'email', 'first_name', 'last_name', 'course', 'position', 'photo', )
        # labels = {
        #     'topic_text': _('Topic of meeting'),
        #     'detail_text': _('Description of meeting'),
        #     'meeting_date': _('Date of meeting')
        # }
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
    first_name = CharField(max_length=50, validators=[alphabetic])
    last_name = CharField(max_length=50, validators=[alphabetic])
    email = EmailField(required=False)
    password = CharField(max_length=12, widget=PasswordInput, validators=[alphanumeric], required=False)

    class Meta:
        model = Student
        fields = ('user_name', 'password', 'email', 'first_name', 'last_name', 'course', 'position', 'photo', )
        # labels = {
        #     'topic_text': _('Topic of meeting'),
        #     'detail_text': _('Description of meeting'),
        #     'meeting_date': _('Date of meeting')
        # }
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
    first_name = CharField(max_length=50, validators=[alphabetic])
    last_name = CharField(max_length=50, validators=[alphabetic])
    email = EmailField(required=False)
    password = CharField(max_length=12, widget=PasswordInput, validators=[alphanumeric], required=False)

    class Meta:
        model = Professor
        fields = ('user_name', 'password', 'email', 'first_name', 'last_name', 'academic_title', 'position', 'photo',)
        # labels = {
        #     'topic_text': _('Topic of meeting'),
        #     'detail_text': _('Description of meeting'),
        #     'meeting_date': _('Date of meeting')
        # }
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

