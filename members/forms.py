from django import forms
from .models import Professor, Student
from meetings.models import Report, Meeting


class ReportChangeForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ('meeting', 'name', 'file', )


class MeetingChangeForm(forms.ModelForm):

    class Meta:
        model = Meeting
        fields = ('topic_text', 'detail_text', 'meeting_date', )
