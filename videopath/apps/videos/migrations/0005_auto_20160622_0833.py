# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20160616_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='service',
            field=models.CharField(default=b'none', max_length=255, choices=[(b'none', b'none'), (b'youtube', b'youtube'), (b'vimeo', b'vimeo'), (b'wistia', b'wistia'), (b'brightcove', b'brightcove'), (b'videopath', b'videopath'), (b'custom', b'custom'), (b'movingimages', b'movingimages')]),
        ),
    ]
