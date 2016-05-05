# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2016, 5, 5, 6, 30, 55, 16851), verbose_name=b'date published', editable=False),
        ),
    ]
