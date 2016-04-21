# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meeting_theme_text', models.CharField(max_length=50)),
                ('meeting_detail_text', models.CharField(max_length=500)),
                ('meeting_date', models.DateField(verbose_name=b'time of meeting')),
                ('meeting_pub_date', models.DateField(verbose_name=b'date published')),
            ],
        ),
    ]
