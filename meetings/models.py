from django.db import models
from members.models import Student
import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Meeting(models.Model):
    topic_text = models.CharField(max_length=50)
    detail_text = models.TextField(default='', blank=True)
    meeting_date = models.DateField('date of meeting')

    def __unicode__(self):  # __unicode__ on Python 2
        return self.topic_text


def limit_meeting_date_choices():
    return {'meeting_date__gte': datetime.datetime.utcnow()}


class Report(models.Model):
    meeting = models.ForeignKey(Meeting, limit_choices_to=limit_meeting_date_choices)
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='report_files', blank=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

    def save(self, *args, **kwargs):
        if not self.file:
            if Report.objects.filter(pk=self.pk).exists():
                origin = Report.objects.get(pk=self.pk)
                origin.file.delete(False)
        super(Report, self).save(*args, **kwargs)


@receiver(post_delete, sender=Report)
def file_report_delete_handler(sender, instance, **kwargs):
    # Pass false so ImageField doesn't save the model.
    instance.file.delete(False)



