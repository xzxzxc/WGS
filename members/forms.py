from django.forms import ModelForm, Textarea
from django.forms.extras.widgets import SelectDateWidget
from meetings.models import Report, Meeting
from django.utils.translation import ugettext_lazy as _


class ReportChangeForm(ModelForm):

    class Meta:
        model = Report
        fields = ('meeting', 'name', 'file', )


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
            'detail_text': Textarea(attrs={'cols': 90, 'rows': 10}),
            'meeting_date': SelectDateWidget(),
        }
