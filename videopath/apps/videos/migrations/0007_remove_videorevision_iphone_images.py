# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20160622_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videorevision',
            name='iphone_images',
        ),
    ]
