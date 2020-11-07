# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_remove_videorevision_endscreen_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marker',
            name='overlay_height',
        ),
        migrations.RemoveField(
            model_name='marker',
            name='overlay_width',
        ),
    ]
