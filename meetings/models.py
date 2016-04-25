from django.db import models
from django.contrib.auth.models import User
import datetime


class Meeting(models.Model):
    topic_text = models.CharField(max_length=50)
    detail_text = models.TextField()
    meeting_date = models.DateField('time of meeting')
    pub_date = models.DateField('date published', auto_now=True, editable=False)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.topic_text


def limit_meeting_date_choices():
    return {'meeting_date__gte': datetime.datetime.utcnow()}


class Report(models.Model):
    meeting = models.ForeignKey(Meeting, limit_choices_to=limit_meeting_date_choices)
    author = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='report_files', blank=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

