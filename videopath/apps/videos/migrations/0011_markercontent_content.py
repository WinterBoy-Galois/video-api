# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0010_auto_20160622_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='markercontent',
            name='content',
            field=models.TextField(null=True, blank=True),
        ),
    ]
