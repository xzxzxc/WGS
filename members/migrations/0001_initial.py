# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('academic_title', models.CharField(default=b'none', max_length=15)),
                ('position', models.CharField(default=b'none', max_length=50)),
                ('join_date', models.DateField(auto_now=True, verbose_name=b'date joined')),
                ('photo', models.ImageField(default=b'default.jpg', upload_to=b'professors')),
                ('photo_small', models.ImageField(default=b'default_small.jpg', upload_to=b'professors_small', editable=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.IntegerField(default=3, choices=[(1, b'first'), (2, b'second'), (3, b'third'), (4, b'fourth'), (5, b'fifth'), (6, b'sixth')])),
                ('position', models.CharField(default=b'none', max_length=50)),
                ('join_date', models.DateField(auto_now=True, verbose_name=b'date joined')),
                ('photo', models.ImageField(default=b'default.jpg', upload_to=b'students')),
                ('photo_small', models.ImageField(default=b'default_small.jpg', upload_to=b'students_small', editable=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
