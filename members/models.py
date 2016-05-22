from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from PIL import Image as Img
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to=Q(groups__name='Professors'),
                                related_name='professor')
    first_name_en = models.CharField(max_length=50)
    last_name_en = models.CharField(max_length=50)
    first_name_ua = models.CharField(max_length=50)
    last_name_ua = models.CharField(max_length=50)
    academic_title = models.CharField(max_length=100, choices=(('doctor', _('Doktor of Physics and Mathematics')),
                                                               ('kandidat', _('Kandidat of Physics and Mathematics')),))
    institution = models.CharField(max_length=100, choices=(('TSNUK', _('Taras Shevchenko National University of Kyiv')),))
    position = models.CharField(max_length=100, choices=(('assistant', _('Teaching assistant')),
                                                         ('academic', _('Academic')), ('docent', _('Docent')),
                                                         ('professor', _('Professor')), ))
    interests_en = models.TextField()
    interests_ua = models.TextField()
    join_date = models.DateField('date joined', auto_now=True)
    photo = models.ImageField(upload_to='professors', default='default.jpg')
    photo_small = models.ImageField(upload_to='professors_small', default='default_small.jpg', editable=False)

    def __unicode__(self):  # __unicode__ on Python 2
        return '%s  %s' % (self.first_name_en, self.last_name_en)

    def name_en(self):
        return '%s  %s' % (self.first_name_en, self.last_name_en)

    def name_ua(self):
        return '%s  %s' % (self.first_name_ua, self.last_name_ua)

    def save(self, *args, **kwargs):
        if self.photo:
            if Professor.objects.filter(pk=self.pk).exists():
                if self.photo != Professor.objects.get(pk=self.pk).photo:
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
            else:
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


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to=Q(groups__name='Students'),
                                related_name='student')
    first_name_en = models.CharField(max_length=50)
    last_name_en = models.CharField(max_length=50)
    first_name_ua = models.CharField(max_length=50)
    last_name_ua = models.CharField(max_length=50)
    course = models.IntegerField(default=3, choices=((1, _('first')), (2, _('second')), (3, _('third')), (4, _('fourth')),
                                                     (5, _('fifth')), (6, _('sixth'))))
    institution = models.CharField(max_length=100,
                                   choices=(('TSNUK', _('Taras Shevchenko National University of Kyiv')),
                                            ('UKMA', _('National University of Kyiv-Mohyla Academy'))))
    group = models.CharField(max_length=100, choices=(('HEP', _('HEP')), ('nuclear', _('Nuclear physics')), ))
    interests_en = models.TextField()
    interests_ua = models.TextField()
    join_date = models.DateField('date joined', auto_now=True)
    photo = models.ImageField(upload_to='students', default='default.jpg')
    photo_small = models.ImageField(upload_to='students_small', default='default_small.jpg', editable=False)

    def __unicode__(self):  # __unicode__ on Python 2
        return '%s  %s' % (self.first_name_en, self.last_name_en)

    def name_en(self):
        return '%s  %s' % (self.first_name_en, self.last_name_en)

    def name_ua(self):
        return '%s  %s' % (self.first_name_ua, self.last_name_ua)

    def save(self, *args, **kwargs):
        if self.photo:
            if Student.objects.filter(pk=self.pk).exists():
                if self.photo != Student.objects.get(pk=self.pk).photo:
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
            else:
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


@receiver(post_delete)
def photo_post_delete_handler(sender, instance, **kwargs):
    list_of_models = ('Student', 'Professor')
    if sender.__name__ in list_of_models:
        if instance.photo.name != 'default.jpg':
            instance.photo.delete(False)  # Pass false so ImageField doesn't save the model.
            instance.photo_small.delete(False)

