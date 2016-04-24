from django import forms

from .models import Professor, Student
from meetings.models import Report
import datetime


def limit_pub_date_choices():
    return {'pub_date__lte': datetime.datetime.utcnow()}


class StudentForm(forms.ModelForm):

    class Meta:
        model = Report
        limit_choices_to = limit_pub_date_choices
        fields = ('meeting', 'name', 'file', )
