# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_videostatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='videostatistics',
            name='sessionKey',
            field=models.CharField(db_index=True, max_length=255, blank=True),
        ),
    ]
