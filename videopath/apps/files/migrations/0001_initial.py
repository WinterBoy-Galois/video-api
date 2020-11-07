# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(unique=True, max_length=50, blank=True)),
                ('status', models.SmallIntegerField(default=0, choices=[(0, b'Created. Waiting for upload.'), (1, b'Uploaded.'), (2, b'Processing'), (3, b'Processed.'), (-1, b'Error.')])),
                ('image_type', models.CharField(default=b'marker content', max_length=255, blank=True, choices=[(b'marker content', b'Image for Marker Content'), (b'custom thumbnail', b'Image for custom video thumbnail'), (b'custom logo', b'Image for custom logo on player chrome')])),
                ('width', models.SmallIntegerField(default=0)),
                ('height', models.SmallIntegerField(default=0)),
                ('bytes', models.BigIntegerField(default=0)),
                ('original_file_name', models.CharField(max_length=255, blank=True)),
                ('markercontent', models.ManyToManyField(related_name='image_file', to='videos.MarkerContent', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
