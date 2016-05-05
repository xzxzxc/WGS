from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Meeting(models.Model):
    topic_text = models.CharField(max_length=50)
    detail_text = models.TextField(default='')
    meeting_date = models.DateField('date of meeting')

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


@receiver(post_delete, sender=Report)
def file_report_delete_handler(sender, instance, **kwargs):
    # Pass false so ImageField doesn't save the model.
    instance.file.delete(False)



