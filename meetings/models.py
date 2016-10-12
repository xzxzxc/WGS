from django.db import models
from members.models import Student
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class Meeting(models.Model):
    topic_text = models.CharField(max_length=50)
    detail_text = models.TextField(default='', blank=True)
    meeting_date = models.DateField('date of meeting')

    def __unicode__(self):  # __unicode__ on Python 2
        return self.topic_text


class Report(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    author_first_name_en = models.CharField(max_length=50, blank=True, null=True)
    author_last_name_en = models.CharField(max_length=50, blank=True, null=True)
    author_first_name_ua = models.CharField(max_length=50, blank=True, null=True)
    author_last_name_ua = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='report_files', blank=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

    def author_name_en(self):
        if self.author is not None:
            if self.author.groups.filter(name='Students').exists():
                return self.author.student.first_name_en + ' ' + self.author.student.last_name_en
            elif self.author.groups.filter(name='Professors').exists():
                return self.author.professor.first_name_en + ' ' + self.author.professor.last_name_en
        else:
            return self.author_first_name_en + ' ' + self.author_last_name_en

    def author_name_ua(self):
        if self.author is not None:
            if self.author.groups.filter(name='Students').exists():
                return self.author.student.first_name_ua + ' ' + self.author.student.last_name_ua
            elif self.author.groups.filter(name='Professors').exists():
                return self.author.professor.first_name_ua + ' ' + self.author.professor.last_name_ua
        else:
            return self.author_first_name_ua + ' ' + self.author_last_name_ua

    def save(self, *args, **kwargs):
        if not self.file:
            if Report.objects.filter(pk=self.pk).exists():
                origin = Report.objects.get(pk=self.pk)
                origin.file.delete(False)
        if self.author_first_name_en:
            self.author=None
        super(Report, self).save(*args, **kwargs)

    def clean(self):
        # Report must have author or author name
        numNone=0
        numNotNone=0
        for i in (self.author_first_name_en, self.author_last_name_en, self.author_first_name_ua, self.author_last_name_ua):
            if not i:
                numNone+=1
            else:
                numNotNone+=1
        if numNotNone>0 and numNone>0:
            raise ValidationError(_('Not registered report author must have first and last names in Ua and En'))


@receiver(post_delete, sender=Report)
def file_report_delete_handler(sender, instance, **kwargs):
    # Pass false so ImageField doesn't save the model.
    instance.file.delete(False)


# @receiver(post_delete, sender=Meeting)
# def meeting_report_delete_handler(sender, instance, **kwargs):
#     # Pass false so ImageField doesn't save the model.
#     for report in Report.objects.filter(meeting=instance):
#         del report
