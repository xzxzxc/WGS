# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_auto_20160505_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='pub_date',
            field=models.DateField(auto_now=True, verbose_name=b'date published'),
        ),
    ]
