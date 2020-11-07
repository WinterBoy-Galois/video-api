# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_auto_20160622_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videorevision',
            name='endscreen_url',
        ),
    ]
