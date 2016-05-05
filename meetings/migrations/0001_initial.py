# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_text', models.CharField(max_length=50)),
                ('detail_text', models.TextField(default=b'')),
                ('meeting_date', models.DateField(verbose_name=b'date of meeting')),
                ('pub_date', models.DateField(default=datetime.datetime(2016, 5, 5, 6, 30, 44, 150981), verbose_name=b'date published', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=b'report_files', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('meeting', models.ForeignKey(to='meetings.Meeting')),
            ],
        ),
    ]
