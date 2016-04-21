# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_auto_20160421_1441'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='meeting_pub_date',
            new_name='pub_date',
        ),
    ]
