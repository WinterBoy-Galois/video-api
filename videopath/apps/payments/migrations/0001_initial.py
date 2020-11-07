# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('exported_invoice', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('charging_attempts', models.IntegerField(default=0)),
                ('last_charging_attempt', models.DateField(null=True)),
                ('provider', models.CharField(default=b'stripe', max_length=150, choices=[(b'other', b'other'), (b'stripe', b'stripe'), (b'transfer', b'transfer')])),
                ('transaction_id', models.CharField(default=b'', max_length=150)),
                ('amount_due', models.IntegerField(default=0)),
                ('percent_vat', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('number', models.IntegerField(default=0)),
                ('currency', models.CharField(default=b'EUR', max_length=3, choices=[(b'USD', b'US Dollars'), (b'GBP', b'British Pounds'), (b'EUR', b'Euro')])),
                ('details', models.CharField(max_length=2048)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('street', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('post_code', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=150, choices=[(b'Afghanistan', b'Afghanistan'), (b'Aland Islands', b'Aland Islands'), (b'Albania', b'Albania'), (b'Algeria', b'Algeria'), (b'American Samoa', b'American Samoa'), (b'AndorrA', b'AndorrA'), (b'Angola', b'Angola'), (b'Anguilla', b'Anguilla'), (b'Antarctica', b'Antarctica'), (b'Antigua and Barbuda', b'Antigua and Barbuda'), (b'Argentina', b'Argentina'), (b'Armenia', b'Armenia'), (b'Aruba', b'Aruba'), (b'Australia', b'Australia'), (b'Austria', b'Austria'), (b'Azerbaijan', b'Azerbaijan'), (b'Bahamas', b'Bahamas'), (b'Bahrain', b'Bahrain'), (b'Bangladesh', b'Bangladesh'), (b'Barbados', b'Barbados'), (b'Belarus', b'Belarus'), (b'Belgium', b'Belgium'), (b'Belize', b'Belize'), (b'Benin', b'Benin'), (b'Bermuda', b'Bermuda'), (b'Bhutan', b'Bhutan'), (b'Bolivia', b'Bolivia'), (b'Bosnia and Herzegovina', b'Bosnia and Herzegovina'), (b'Botswana', b'Botswana'), (b'Bouvet Island', b'Bouvet Island'), (b'Brazil', b'Brazil'), (b'British Indian Ocean Territory', b'British Indian Ocean Territory'), (b'Brunei Darussalam', b'Brunei Darussalam'), (b'Bulgaria', b'Bulgaria'), (b'Burkina Faso', b'Burkina Faso'), (b'Burundi', b'Burundi'), (b'Cambodia', b'Cambodia'), (b'Cameroon', b'Cameroon'), (b'Canada', b'Canada'), (b'Cape Verde', b'Cape Verde'), (b'Cayman Islands', b'Cayman Islands'), (b'Central African Republic', b'Central African Republic'), (b'Chad', b'Chad'), (b'Chile', b'Chile'), (b'China', b'China'), (b'Christmas Island', b'Christmas Island'), (b'Cocos (Keeling) Islands', b'Cocos (Keeling) Islands'), (b'Colombia', b'Colombia'), (b'Comoros', b'Comoros'), (b'Congo', b'Congo'), (b'Congo, The Democratic Republic of the', b'Congo, The Democratic Republic of the'), (b'Cook Islands', b'Cook Islands'), (b'Costa Rica', b'Costa Rica'), (b'Cote D"Ivoire', b'Cote D"Ivoire'), (b'Croatia', b'Croatia'), (b'Cuba', b'Cuba'), (b'Cyprus', b'Cyprus'), (b'Czech Republic', b'Czech Republic'), (b'Denmark', b'Denmark'), (b'Djibouti', b'Djibouti'), (b'Dominica', b'Dominica'), (b'Dominican Republic', b'Dominican Republic'), (b'Ecuador', b'Ecuador'), (b'Egypt', b'Egypt'), (b'El Salvador', b'El Salvador'), (b'Equatorial Guinea', b'Equatorial Guinea'), (b'Eritrea', b'Eritrea'), (b'Estonia', b'Estonia'), (b'Ethiopia', b'Ethiopia'), (b'Falkland Islands (Malvinas)', b'Falkland Islands (Malvinas)'), (b'Faroe Islands', b'Faroe Islands'), (b'Fiji', b'Fiji'), (b'Finland', b'Finland'), (b'France', b'France'), (b'French Guiana', b'French Guiana'), (b'French Polynesia', b'French Polynesia'), (b'French Southern Territories', b'French Southern Territories'), (b'Gabon', b'Gabon'), (b'Gambia', b'Gambia'), (b'Georgia', b'Georgia'), (b'Germany', b'Germany'), (b'Ghana', b'Ghana'), (b'Gibraltar', b'Gibraltar'), (b'Greece', b'Greece'), (b'Greenland', b'Greenland'), (b'Grenada', b'Grenada'), (b'Guadeloupe', b'Guadeloupe'), (b'Guam', b'Guam'), (b'Guatemala', b'Guatemala'), (b'Guernsey', b'Guernsey'), (b'Guinea', b'Guinea'), (b'Guinea-Bissau', b'Guinea-Bissau'), (b'Guyana', b'Guyana'), (b'Haiti', b'Haiti'), (b'Heard Island and Mcdonald Islands', b'Heard Island and Mcdonald Islands'), (b'Holy See (Vatican City State)', b'Holy See (Vatican City State)'), (b'Honduras', b'Honduras'), (b'Hong Kong', b'Hong Kong'), (b'Hungary', b'Hungary'), (b'Iceland', b'Iceland'), (b'India', b'India'), (b'Indonesia', b'Indonesia'), (b'Iran, Islamic Republic Of', b'Iran, Islamic Republic Of'), (b'Iraq', b'Iraq'), (b'Ireland', b'Ireland'), (b'Isle of Man', b'Isle of Man'), (b'Israel', b'Israel'), (b'Italy', b'Italy'), (b'Jamaica', b'Jamaica'), (b'Japan', b'Japan'), (b'Jersey', b'Jersey'), (b'Jordan', b'Jordan'), (b'Kazakhstan', b'Kazakhstan'), (b'Kenya', b'Kenya'), (b'Kiribati', b'Kiribati'), (b'Korea, Democratic People"S Republic of', b'Korea, Democratic People"S Republic of'), (b'Korea, Republic of', b'Korea, Republic of'), (b'Kuwait', b'Kuwait'), (b'Kyrgyzstan', b'Kyrgyzstan'), (b'Lao People"S Democratic Republic', b'Lao People"S Democratic Republic'), (b'Latvia', b'Latvia'), (b'Lebanon', b'Lebanon'), (b'Lesotho', b'Lesotho'), (b'Liberia', b'Liberia'), (b'Libyan Arab Jamahiriya', b'Libyan Arab Jamahiriya'), (b'Liechtenstein', b'Liechtenstein'), (b'Lithuania', b'Lithuania'), (b'Luxembourg', b'Luxembourg'), (b'Macao', b'Macao'), (b'Macedonia, The Former Yugoslav Republic of', b'Macedonia, The Former Yugoslav Republic of'), (b'Madagascar', b'Madagascar'), (b'Malawi', b'Malawi'), (b'Malaysia', b'Malaysia'), (b'Maldives', b'Maldives'), (b'Mali', b'Mali'), (b'Malta', b'Malta'), (b'Marshall Islands', b'Marshall Islands'), (b'Martinique', b'Martinique'), (b'Mauritania', b'Mauritania'), (b'Mauritius', b'Mauritius'), (b'Mayotte', b'Mayotte'), (b'Mexico', b'Mexico'), (b'Micronesia, Federated States of', b'Micronesia, Federated States of'), (b'Moldova, Republic of', b'Moldova, Republic of'), (b'Monaco', b'Monaco'), (b'Mongolia', b'Mongolia'), (b'Montserrat', b'Montserrat'), (b'Morocco', b'Morocco'), (b'Mozambique', b'Mozambique'), (b'Myanmar', b'Myanmar'), (b'Namibia', b'Namibia'), (b'Nauru', b'Nauru'), (b'Nepal', b'Nepal'), (b'Netherlands', b'Netherlands'), (b'Netherlands Antilles', b'Netherlands Antilles'), (b'New Caledonia', b'New Caledonia'), (b'New Zealand', b'New Zealand'), (b'Nicaragua', b'Nicaragua'), (b'Niger', b'Niger'), (b'Nigeria', b'Nigeria'), (b'Niue', b'Niue'), (b'Norfolk Island', b'Norfolk Island'), (b'Northern Mariana Islands', b'Northern Mariana Islands'), (b'Norway', b'Norway'), (b'Oman', b'Oman'), (b'Pakistan', b'Pakistan'), (b'Palau', b'Palau'), (b'Palestinian Territory, Occupied', b'Palestinian Territory, Occupied'), (b'Panama', b'Panama'), (b'Papua New Guinea', b'Papua New Guinea'), (b'Paraguay', b'Paraguay'), (b'Peru', b'Peru'), (b'Philippines', b'Philippines'), (b'Pitcairn', b'Pitcairn'), (b'Poland', b'Poland'), (b'Portugal', b'Portugal'), (b'Puerto Rico', b'Puerto Rico'), (b'Qatar', b'Qatar'), (b'Reunion', b'Reunion'), (b'Romania', b'Romania'), (b'Russian Federation', b'Russian Federation'), (b'RWANDA', b'RWANDA'), (b'Saint Helena', b'Saint Helena'), (b'Saint Kitts and Nevis', b'Saint Kitts and Nevis'), (b'Saint Lucia', b'Saint Lucia'), (b'Saint Pierre and Miquelon', b'Saint Pierre and Miquelon'), (b'Saint Vincent and the Grenadines', b'Saint Vincent and the Grenadines'), (b'Samoa', b'Samoa'), (b'San Marino', b'San Marino'), (b'Sao Tome and Principe', b'Sao Tome and Principe'), (b'Saudi Arabia', b'Saudi Arabia'), (b'Senegal', b'Senegal'), (b'Serbia and Montenegro', b'Serbia and Montenegro'), (b'Seychelles', b'Seychelles'), (b'Sierra Leone', b'Sierra Leone'), (b'Singapore', b'Singapore'), (b'Slovakia', b'Slovakia'), (b'Slovenia', b'Slovenia'), (b'Solomon Islands', b'Solomon Islands'), (b'Somalia', b'Somalia'), (b'South Africa', b'South Africa'), (b'South Georgia and the South Sandwich Islands', b'South Georgia and the South Sandwich Islands'), (b'Spain', b'Spain'), (b'Sri Lanka', b'Sri Lanka'), (b'Sudan', b'Sudan'), (b'Suriname', b'Suriname'), (b'Svalbard and Jan Mayen', b'Svalbard and Jan Mayen'), (b'Swaziland', b'Swaziland'), (b'Sweden', b'Sweden'), (b'Switzerland', b'Switzerland'), (b'Syrian Arab Republic', b'Syrian Arab Republic'), (b'Taiwan, Province of China', b'Taiwan, Province of China'), (b'Tajikistan', b'Tajikistan'), (b'Tanzania, United Republic of', b'Tanzania, United Republic of'), (b'Thailand', b'Thailand'), (b'Timor-Leste', b'Timor-Leste'), (b'Togo', b'Togo'), (b'Tokelau', b'Tokelau'), (b'Tonga', b'Tonga'), (b'Trinidad and Tobago', b'Trinidad and Tobago'), (b'Tunisia', b'Tunisia'), (b'Turkey', b'Turkey'), (b'Turkmenistan', b'Turkmenistan'), (b'Turks and Caicos Islands', b'Turks and Caicos Islands'), (b'Tuvalu', b'Tuvalu'), (b'Uganda', b'Uganda'), (b'Ukraine', b'Ukraine'), (b'United Arab Emirates', b'United Arab Emirates'), (b'United Kingdom', b'United Kingdom'), (b'United States', b'United States'), (b'United States Minor Outlying Islands', b'United States Minor Outlying Islands'), (b'Uruguay', b'Uruguay'), (b'Uzbekistan', b'Uzbekistan'), (b'Vanuatu', b'Vanuatu'), (b'Venezuela', b'Venezuela'), (b'Viet Nam', b'Viet Nam'), (b'Virgin Islands, British', b'Virgin Islands, British'), (b'Virgin Islands, U.S.', b'Virgin Islands, U.S.'), (b'Wallis and Futuna', b'Wallis and Futuna'), (b'Western Sahara', b'Western Sahara'), (b'Yemen', b'Yemen'), (b'Zambia', b'Zambia'), (b'Zimbabwe', b'Zimbabwe')])),
                ('vat_id', models.CharField(default=b'', max_length=150, null=True, blank=True)),
                ('email', models.CharField(default=b'', max_length=150, null=True, blank=True)),
                ('notes', models.TextField(default=b'', null=True, blank=True)),
                ('user', models.OneToOneField(related_name='payment_details', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name=b'user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PendingSubscription',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('plan', models.CharField(max_length=150, choices=[(b'individual-moodfilm', b'0001 Moodfilm enterprise (individual-moodfilm)'), (b'free-free', b'1000 Free (free-free)'), (b'201509-starter-monthly-15', b'2001 Basic Monthly (201509-starter-monthly-15)'), (b'201509-starter-monthly-25', b'2001 Basic Monthly (201509-starter-monthly-25)'), (b'201509-starter-monthly-20-discount', b'2002 Basic Monthly (20% Partners Discount) (201509-starter-monthly-20-discount)'), (b'201509-starter-monthly', b'2003 Basic Monthly (201509-starter-monthly)'), (b'201509-starter-yearly-20-discount', b'2004 Basic Yearly (20% Partners Discount) (201509-starter-yearly-20-discount)'), (b'201509-starter-yearly', b'2005 Basic Yearly (201509-starter-yearly)'), (b'201412-pro-plus-monthly-25-jobviddy', b'4001 Professional Monthly (25% Discount) Andy (201412-pro-plus-monthly-25-jobviddy)'), (b'201412-pro-plus-monthly-20-discount', b'4002 Professional Monthly (20% Partners Discount) (201412-pro-plus-monthly-20-discount)'), (b'201412-pro-plus-monthly', b'4003 Professional Monthly (201412-pro-plus-monthly)'), (b'201412-pro-plus-yearly-20-discount', b'4004 Professional Yearly (20% Partners Discount) (201412-pro-plus-yearly-20-discount)'), (b'201412-pro-plus-yearly', b'4005 Professional Yearly (201412-pro-plus-yearly)'), (b'201412-enterprise-monthly-20-discount', b'6001 Enterprise Monthly (20% Partners Discount) (201412-enterprise-monthly-20-discount)'), (b'201412-enterprise-monthly', b'6002 Enterprise Monthly (201412-enterprise-monthly)'), (b'201412-enterprise-yearly-20-discount', b'6003 Enterprise Yearly (20% Partners Discount) (201412-enterprise-yearly-20-discount)'), (b'201412-enterprise-yearly', b'6004 Enterprise Yearly (201412-enterprise-yearly)'), (b'individual-individual', b'8000 Individual Plan (individual-individual)'), (b'individual-meisterclass', b'8001 Individual meisterclasss (individual-meisterclass)'), (b'individual-escp', b'8002 Individual escp (individual-escp)'), (b'individual-sspss', b'8003 Individual SSPSS (individual-sspss)'), (b'individual-agency-evaluation', b'8004 Agency Evaluation (individual-agency-evaluation)'), (b'individual-brightcove', b'8005 Pro (individual-brightcove)'), (b'individual-coop', b'8006 Coop Enterprise (individual-coop)'), (b'individual-staff', b'9999 videopath staff account (individual-staff)')])),
                ('user', models.OneToOneField(related_name='pending_subscription', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name=b'user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuotaInformation',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('quota_exceeded', models.BooleanField(default=False)),
                ('warning_sent', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='quota_info', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name=b'user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StripeID',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(unique=True, max_length=50, db_index=True)),
                ('user', models.OneToOneField(related_name='stripe_id', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name=b'user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('plan', models.CharField(default=b'free-free', max_length=150, choices=[(b'individual-moodfilm', b'0001 Moodfilm enterprise (individual-moodfilm)'), (b'free-free', b'1000 Free (free-free)'), (b'201509-starter-monthly-15', b'2001 Basic Monthly (201509-starter-monthly-15)'), (b'201509-starter-monthly-25', b'2001 Basic Monthly (201509-starter-monthly-25)'), (b'201509-starter-monthly-20-discount', b'2002 Basic Monthly (20% Partners Discount) (201509-starter-monthly-20-discount)'), (b'201509-starter-monthly', b'2003 Basic Monthly (201509-starter-monthly)'), (b'201509-starter-yearly-20-discount', b'2004 Basic Yearly (20% Partners Discount) (201509-starter-yearly-20-discount)'), (b'201509-starter-yearly', b'2005 Basic Yearly (201509-starter-yearly)'), (b'201412-pro-plus-monthly-25-jobviddy', b'4001 Professional Monthly (25% Discount) Andy (201412-pro-plus-monthly-25-jobviddy)'), (b'201412-pro-plus-monthly-20-discount', b'4002 Professional Monthly (20% Partners Discount) (201412-pro-plus-monthly-20-discount)'), (b'201412-pro-plus-monthly', b'4003 Professional Monthly (201412-pro-plus-monthly)'), (b'201412-pro-plus-yearly-20-discount', b'4004 Professional Yearly (20% Partners Discount) (201412-pro-plus-yearly-20-discount)'), (b'201412-pro-plus-yearly', b'4005 Professional Yearly (201412-pro-plus-yearly)'), (b'201412-enterprise-monthly-20-discount', b'6001 Enterprise Monthly (20% Partners Discount) (201412-enterprise-monthly-20-discount)'), (b'201412-enterprise-monthly', b'6002 Enterprise Monthly (201412-enterprise-monthly)'), (b'201412-enterprise-yearly-20-discount', b'6003 Enterprise Yearly (20% Partners Discount) (201412-enterprise-yearly-20-discount)'), (b'201412-enterprise-yearly', b'6004 Enterprise Yearly (201412-enterprise-yearly)'), (b'individual-individual', b'8000 Individual Plan (individual-individual)'), (b'individual-meisterclass', b'8001 Individual meisterclasss (individual-meisterclass)'), (b'individual-escp', b'8002 Individual escp (individual-escp)'), (b'individual-sspss', b'8003 Individual SSPSS (individual-sspss)'), (b'individual-agency-evaluation', b'8004 Agency Evaluation (individual-agency-evaluation)'), (b'individual-brightcove', b'8005 Pro (individual-brightcove)'), (b'individual-coop', b'8006 Coop Enterprise (individual-coop)'), (b'individual-staff', b'9999 videopath staff account (individual-staff)')])),
                ('active', models.BooleanField(default=True)),
                ('managed_by', models.CharField(default=b'admin', max_length=255, choices=[(b'admin', b'admin'), (b'system', b'system')])),
                ('current_period_start', models.DateField(null=True, blank=True)),
                ('current_period_end', models.DateField(null=True, blank=True)),
                ('price', models.IntegerField(default=-1)),
                ('currency', models.CharField(default=b'EUR', max_length=3, choices=[(b'USD', b'US Dollars'), (b'GBP', b'British Pounds'), (b'EUR', b'Euro')])),
                ('user', models.OneToOneField(related_name='subscription', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name=b'user')),
                ('notes', models.TextField(default=b'')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(related_name='payments', to=settings.AUTH_USER_MODEL),
        ),
    ]
