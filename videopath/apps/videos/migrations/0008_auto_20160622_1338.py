# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_remove_videorevision_iphone_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videorevision',
            name='tracking_pixel_end',
        ),
        migrations.RemoveField(
            model_name='videorevision',
            name='tracking_pixel_q1',
        ),
        migrations.RemoveField(
            model_name='videorevision',
            name='tracking_pixel_q2',
        ),
        migrations.RemoveField(
            model_name='videorevision',
            name='tracking_pixel_q3',
        ),
        migrations.RemoveField(
            model_name='videorevision',
            name='tracking_pixel_start',
        ),
    ]
