from django.db import models
from django.utils import timezone


class Member(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50, default='none')
    join_date = models.DateField('date joined', default=timezone.now())

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


class Professor(Member):
    academic_title = models.CharField(max_length=15, default='none')


class Student(Member):
    course = models.IntegerField(default=3)

