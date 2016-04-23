from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image as Img
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Professor(models.Model):
    user = models.OneToOneField(User, default=2, on_delete=models.CASCADE)
    academic_title = models.CharField(max_length=15, default='none')
    position = models.CharField(max_length=50, default='none')
    join_date = models.DateField('date joined', auto_now=True)
    photo = models.ImageField(upload_to='pofessors', default='default.jpg')
    photo_small = models.ImageField(upload_to='professors_small', default='default_small.jpg', editable=False)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.user.username

    def save(self, *args, **kwargs):
        if self.photo:
            image = Img.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((200, 200), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.photo.name, 'image/jpeg',
                                              output.len, None)
            image = Img.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((50, 50), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo_small = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.photo.name, 'image/jpeg',
                                                    output.len, None)
        super(Professor, self).save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(User, default=2, on_delete=models.CASCADE)
    course = models.IntegerField(default=3)
    position = models.CharField(max_length=50, default='none')
    join_date = models.DateField('date joined', auto_now=True)
    photo = models.ImageField(upload_to='students', default='default.jpg')
    photo_small = models.ImageField(upload_to='students_small', default='default_small.jpg', editable=False)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.user.username

    def save(self, *args, **kwargs):
        if self.photo:
            image = Img.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((200, 200), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.photo.name, 'image/jpeg',
                                              output.len, None)
            image = Img.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((50, 50), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo_small = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.photo.name, 'image/jpeg',
                                                    output.len, None)
        super(Student, self).save(*args, **kwargs)
