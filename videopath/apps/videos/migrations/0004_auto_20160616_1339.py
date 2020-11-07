# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_videorevision_ui_enable_mobile_portrait'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videorevision',
            name='ui_enable_mobile_portrait',
            field=models.BooleanField(default=True),
        ),
    ]
