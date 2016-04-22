from django.db import models
from django.utils import timezone
import datetime


class Meeting(models.Model):
    topic_text = models.CharField(max_length=50)
    detail_text = models.TextField()
    meeting_date = models.DateField('time of meeting')
    pub_date = models.DateField('date published')

    def __unicode__(self):  # __unicode__ on Python 2
        return self.topic_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

        was_published_recently.admin_order_field = 'pub_date'
        was_published_recently.boolean = True


class Report(models.Model):
    meeting = models.ForeignKey(Meeting)
    author = models.ForeignKey('members.Member')
    name = models.CharField(max_length=50)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name
