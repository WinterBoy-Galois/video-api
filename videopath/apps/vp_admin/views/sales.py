from .decorators import group_membership_required
from django.http import HttpResponse
import csv
import datetime
from urlparse import urlparse
from django.shortcuts import redirect

from django.template.response import SimpleTemplateResponse
from videopath.apps.users.models import User
from videopath.apps.videos.models import Video

from videopath.apps.users.actions import move_user_to_pipedrive

from .helpers import table

BASE_URL = '/admin/sales/inbound-users/'
PIPEDRIVE_PERSON_URL = 'https://videopath.pipedrive.com/person/'

def referral_link(url):
        if url:
            parsed_uri = urlparse( url )
            return '<a href="' + url + '">' + parsed_uri.netloc +'</a><br />';
        return ''

def build_csv_response(data):
	response = HttpResponse(content_type='text/csv') 
	writer = csv.writer(response)

	for row in data:
		writer.writerow(row)

	return response

def export_user_to_pipedrive(pk):
	try:
		user = User.objects.get(pk=pk)
		move_user_to_pipedrive.run(user)
	except:
		pass

@group_membership_required('exports')
def inbound_users(request):

	rows = []

	header = ['ID', 'Email', 'Phone', 'Date Joined',
		 'Country', 'Referrer', 'Campaign',
		 'Created', 'Published', 'Plan', 'Pipedrive', 'Retentionmails', 'Pro Demo', 
		]

	days = int(request.GET.get('days', 14))
	date = datetime.date.today() - datetime.timedelta(days=days)


	#
	# Toggle pipedrive export
	#
	pipedrive_export = int(request.GET.get('pipedrive', -1))
	export_user_to_pipedrive(pipedrive_export)

	#
	# toggle retention
	#
	change_mail_settings = int(request.GET.get('retention', -1))
	change_mail_value = int(request.GET.get('value', -1))

	if change_mail_settings > 0:
		u = User.objects.get(pk=change_mail_settings)
		u.settings.receive_retention_emails = True if change_mail_value else False
		u.settings.save()

	if len(request.GET):
		return redirect(BASE_URL)

	# build row from user
	for user in User.objects.select_related('sales_info').select_related('settings').select_related('campaign_data').filter(date_joined__gte=date).order_by('-date_joined'):

		try:
			phone = user.settings.phone_number
		except:
			phone = ''

		# standard data
		row = [user.pk, user.username,  phone, user.date_joined.date()]

		# signup data
		try:
			row.extend([user.campaign_data.country, referral_link(user.campaign_data.referrer), user.campaign_data.name])
		except:
			row.extend(['', '', ''])

		user_videos = Video.objects.filter(team__owner=user)
		row.extend([user_videos.count(), user_videos.filter(published=True).count()]  )

		try:
			row.append(user.subscription.plan)
		except: 
			row.append('-')

		# pipedrive info
		try:
			url = PIPEDRIVE_PERSON_URL + str(user.sales_info.pipedrive_person_id)
			row.append('<a target = "_blank" href = "{0}">Linked</a>'.format(url))
		except:
			url = BASE_URL + '?pipedrive=' + str(user.pk)
			row.append('<a href = "{0}">Export</a>'.format(url))

		url = BASE_URL + '?retention=' + str(user.pk) +'&value=' + ('0' if user.settings.receive_retention_emails else '1')
		title = 'Enabled' if user.settings.receive_retention_emails else 'Disabled'
		row.append('<a href = "{0}">{1}</a>'.format(url, title))
		row.append('Upgrade (15 days)')




		rows.append(row)


	return SimpleTemplateResponse("insights/base.html", {
	    "title": "Inbound Users",
	    "insight_content": table(rows, header)
	    })
