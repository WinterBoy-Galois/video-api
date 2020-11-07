# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Integration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('service', models.CharField(default=b'', max_length=255, choices=[(b'mailchimp', b'mailchimp'), (b'vimeo', b'vimeo'), (b'brightcove', b'brightcove')])),
                ('credentials', models.CharField(max_length=2048, blank=True)),
                ('settings', models.CharField(max_length=2048, blank=True)),
                ('team', models.ForeignKey(related_name='integrations', to='users.Team')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='integration',
            unique_together=set([('team', 'service')]),
        ),
    ]
