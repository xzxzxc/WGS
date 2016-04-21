# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_auto_20160421_1459'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='meeting_detail_text',
            new_name='detail_text',
        ),
        migrations.RenameField(
            model_name='meeting',
            old_name='meeting_theme_text',
            new_name='theme_text',
        ),
    ]
