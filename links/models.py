from django.db import models
from members.models import Professor
from django.db.models.signals import post_delete
from django.dispatch import receiver
from WGS.settings import MEDIA_ROOT
import shutil
import os


class Dir(models.Model):
    name = models.CharField(max_length=15, unique=True)
    author = models.ForeignKey(Professor, on_delete=models.CASCADE, editable=False)
    description = models.CharField(max_length=300, blank=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

    def save(self, *args, **kwargs):
        if not os.path.exists('%slinks/%s' % (MEDIA_ROOT, self.name)):
            os.makedirs('%slinks/%s' % (MEDIA_ROOT, self.name))
        super(Dir, self).save(*args, **kwargs)


def get_upload_to(self, filename):
    return 'links/%s/%s' % (self.dir.name, filename)


class File(models.Model):
    dir = models.ForeignKey(Dir, editable=False)
    file = models.FileField(upload_to=get_upload_to)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.file.name.split('/')[-1]


@receiver(post_delete, sender=File)
def file_report_delete_handler(sender, instance, **kwargs):
    # Pass false so ImageField doesn't save the model.
    instance.file.delete(False)


@receiver(post_delete, sender=Dir)
def dir_report_delete_handler(sender, instance, **kwargs):
    shutil.rmtree('%slinks/%s' % (MEDIA_ROOT, instance.name))
