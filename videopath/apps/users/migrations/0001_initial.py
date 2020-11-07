# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import easy_thumbnails.fields
from django.conf import settings
import userena.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthenticationToken',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('last_used', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AutomatedMail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('mailtype', models.CharField(default=b'', max_length=20, choices=[(b'welcome', b'welcome'), (b'follow_up_21', b'follow_up_21'), (b'follow_up_42', b'follow_up_42')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OneTimeAuthenticationToken',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('token', models.ForeignKey(related_name='onetime_tokens', to='users.AuthenticationToken')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default=b'My Projects', max_length=150)),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(default=b'editor', max_length=20, choices=[(b'editor', b'editor'), (b'admin', b'admin')])),
                ('team', models.ForeignKey(to='users.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('last_seen', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserActivityDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('day', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCampaignData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('source', models.CharField(default=b'', max_length=512, null=True)),
                ('medium', models.CharField(default=b'', max_length=512, null=True)),
                ('name', models.CharField(default=b'', max_length=512, null=True)),
                ('content', models.CharField(default=b'', max_length=512, null=True)),
                ('term', models.CharField(default=b'', max_length=512, null=True)),
                ('country', models.CharField(default=b'', max_length=512, null=True)),
                ('referrer', models.CharField(default=b'', max_length=512, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserSalesInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('pipedrive_person_id', models.IntegerField(default=-1, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'registered', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('currency', models.CharField(default=b'EUR', max_length=3, choices=[(b'USD', b'US Dollars'), (b'GBP', b'British Pounds'), (b'EUR', b'Euro')])),
                ('payment_provider', models.CharField(default=b'stripe', max_length=150, choices=[(b'other', b'other'), (b'stripe', b'stripe'), (b'transfer', b'transfer')])),
                ('phone_number', models.CharField(default=b'', max_length=100)),
                ('receive_system_emails', models.BooleanField(default=True)),
                ('receive_retention_emails', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'User Settings',
                'verbose_name_plural': 'User Settings',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='usersettings',
            name='user',
            field=models.OneToOneField(related_name='settings', verbose_name=b'user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersalesinfo',
            name='user',
            field=models.OneToOneField(related_name='sales_info', verbose_name=b'user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usercampaigndata',
            name='user',
            field=models.OneToOneField(related_name='campaign_data', verbose_name=b'user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='useractivityday',
            name='user',
            field=models.ForeignKey(related_name='user_activity_day', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='useractivity',
            name='user',
            field=models.OneToOneField(related_name='activity', verbose_name=b'user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='teammember',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='is_default_team_of_user',
            field=models.OneToOneField(related_name='default_team', null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name=b'default_team_of_user'),
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='users.TeamMember'),
        ),
        migrations.AddField(
            model_name='team',
            name='owner',
            field=models.ForeignKey(related_name='owned_teams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='automatedmail',
            name='user',
            field=models.ForeignKey(related_name='automated_mails', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='authenticationtoken',
            name='user',
            field=models.ForeignKey(related_name='authentication_tokens', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='useractivityday',
            unique_together=set([('user', 'day')]),
        ),
    ]
