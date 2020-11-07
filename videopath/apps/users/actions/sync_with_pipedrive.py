#
# Mark all users which are also in pipedrive as contacted, therefor disable the 1 week welcome emails
#

import requests

from django.conf import settings

from videopath.apps.users.models import User, UserSalesInfo

PIPEDRIVE_API_KEY = settings.PIPEDRIVE_API_KEY
PIPEDRIVE_BASE_URL = 'https://api.pipedrive.com/v1'
PIPEDRIVE_PERSON_URL = PIPEDRIVE_BASE_URL + '/persons'


def run():
	
	params = {
		'api_token': PIPEDRIVE_API_KEY,
		'sort': 'add_time DESC, email ASC',
		'limit': 1000
	}
	persons = requests.get(PIPEDRIVE_PERSON_URL, params=params).json()

	for u in persons['data']:

		email = u['email'][0]['value']
		pipedrive_id = u['id']

		if not email or email == '':
			continue
		try:
			email = email.strip()
			user = User.objects.get(email=email)
			info, created = UserSalesInfo.objects.get_or_create(user=user)
			info.pipedrive_person_id = pipedrive_id
			info.save()
		except User.DoesNotExist:
			pass		

