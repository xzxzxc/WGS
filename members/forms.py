from django import forms
from .models import Professor, Student
from meetings.models import Report


class StudentForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ('meeting', 'name', 'file', )
