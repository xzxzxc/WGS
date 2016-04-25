from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from PIL import Image as Img
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.core.urlresolvers import reverse


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to=Q(groups__name='Professors'))
    academic_title = models.CharField(max_length=15, default='none')
    position = models.CharField(max_length=50, default='none')
    join_date = models.DateField('date joined', auto_now=True)
    photo = models.ImageField(upload_to='professors', default='default.jpg')
    photo_small = models.ImageField(upload_to='professors_small', default='default_small.jpg', editable=False)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.user.username

    def name(self):
        return self.user.first_name + '  ' + self.user.last_name

    def save(self, *args, **kwargs):
        if self.photo and self.photo.name != 'default.jpg':
            image = Img.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((200, 200), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output, 'ImageField', "%s" % self.photo.name, 'image/jpeg',
                                              output.len, None)
            image = Img.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((50, 50), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo_small = InMemoryUploadedFile(output, 'ImageField', "%s" % self.photo.name, 'image/jpeg',
                                                    output.len, None)
        super(Professor, self).save(*args, **kwargs)

    def clean(self):
        if self.user.first_name == '':
            raise ValidationError(_('User for this professor might have first name'))
        if self.user.last_name == '':
            raise ValidationError(_('User for this professor might have last name'))


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to=Q(groups__name='Students'))
    course = models.IntegerField(default=3)
    position = models.CharField(max_length=50, default='none')
    join_date = models.DateField('date joined', auto_now=True)
    photo = models.ImageField(upload_to='students', default='default.jpg')
    photo_small = models.ImageField(upload_to='students_small', default='default_small.jpg', editable=False)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.user.username

    def name(self):
        return self.user.first_name + '  ' + self.user.last_name

    def save(self, *args, **kwargs):
        if self.photo and self.photo.name != 'default.jpg':
            image = Img.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((200, 200), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output, 'ImageField', "%s" % self.photo.name, 'image/jpeg',
                                              output.len, None)
            image = Img.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((50, 50), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo_small = InMemoryUploadedFile(output, 'ImageField', "%s" % self.photo.name, 'image/jpeg',
                                                    output.len, None)
        super(Student, self).save(*args, **kwargs)

    def clean(self):
        if self.user.first_name == '':
            raise ValidationError(_('User for this student might have first name'))
        if self.user.last_name == '':
            raise ValidationError(_('User for this student might have last name'))
