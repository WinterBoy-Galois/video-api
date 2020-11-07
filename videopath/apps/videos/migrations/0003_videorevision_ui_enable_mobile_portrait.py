# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_videorevision_custom_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='videorevision',
            name='ui_enable_mobile_portrait',
            field=models.BooleanField(default=False),
        ),
    ]
