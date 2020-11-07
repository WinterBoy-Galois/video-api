# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_apitoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apitoken',
            name='key',
            field=models.CharField(max_length=40, serialize=False, primary_key=True, blank=True),
        ),
    ]
