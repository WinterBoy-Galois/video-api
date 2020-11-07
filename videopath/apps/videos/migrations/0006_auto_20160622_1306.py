# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_auto_20160622_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='jpg_sequence_length',
        ),
        migrations.RemoveField(
            model_name='source',
            name='jpg_sequence_support',
        ),
    ]
