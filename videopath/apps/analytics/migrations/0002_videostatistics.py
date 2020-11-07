# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('playingTotal', models.FloatField(default=0)),
                ('overlayOpenTotal', models.FloatField(default=0)),
                ('progressMax', models.FloatField(default=0)),
                ('sessionTotal', models.FloatField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
