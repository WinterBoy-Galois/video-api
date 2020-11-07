#
# Moves a user into the pipedrive system
#

import requests

from django.conf import settings

from videopath.apps.users.models import UserSalesInfo, UserCampaignData

PIPEDRIVE_API_KEY = settings.PIPEDRIVE_API_KEY

PIPEDRIVE_BASE_URL = 'https://api.pipedrive.com/v1'
INSIGHTS_BASE_URL = 'https://api.videopath.com/admin/insights/users/'

PIPEDRIVE_PERSON_URL = PIPEDRIVE_BASE_URL + '/persons'
PIPEDRIVE_FIND_PERSON_URL = PIPEDRIVE_PERSON_URL + '/find'
PIPEDRIVE_DEAL_URL = PIPEDRIVE_BASE_URL + '/deals'
PIPEDRIVE_ORG_URL = PIPEDRIVE_BASE_URL + '/organizations'
PIPEDRIVE_NOTE_URL = PIPEDRIVE_BASE_URL + '/notes'

DEFAULT_STAGE_ID = 14
SOURCE_FIELD_ID = 'c74438c341d64dadce88fec9796605a73daa2057'
USER_APP_LINK_FIELD_ID = '6d43da07f7a39b393d40dcc48fcda4f41b0feabc'
USER_COUNTRY_FIELD_ID = '027bf82e5f6fcafb475fbd8f7a47c45668e7fc2c'
USER_REFERRER_FIELD_ID = 'd683ac8e5a36c454e67961f3aa5c6b04b1076b79'


USER_ID = 279049 # Anna


def run(user, only_check_and_link = False):

	person_id = _get_person_by_email(user.email)
	if person_id >= 0:
		return _link_user_to_pipedrive_person(user,person_id)
	if only_check_and_link:
		return None
	person_id = _create_person_in_pipedrive(user)
	return _link_user_to_pipedrive_person(user,person_id)


def _link_user_to_pipedrive_person(user, person_id):
	info, created = UserSalesInfo.objects.get_or_create(user=user)
	info.pipedrive_person_id = person_id
	info.save()
	return info

def _get_person_by_email(email):
	params = {
		'term': email,
		'search_by_email': 1
	}
	result = _pipedrive_get(PIPEDRIVE_FIND_PERSON_URL, params)['data']
	
	if result and len(result):
		return result[0].get('id')
	return None 

def _create_person_in_pipedrive(user):

	email = user.email

	try:
		phone = user.settings.phone_number
	except:
		phone = ''

	country = ''
	referrer = ''
	try:
		country = user.campaign_data.country
		referrer = user.campaign_data.referrer
	except UserCampaignData.DoesNotExist: pass

	# create person
	data = {
		'email': email,
		'name': email,
		'visible_to': 3,
		'phone': phone,
		'owner_id': USER_ID,
		USER_APP_LINK_FIELD_ID: INSIGHTS_BASE_URL + user.email + '/',
		USER_COUNTRY_FIELD_ID: country,
		USER_REFERRER_FIELD_ID: referrer
	}
	person_id = _pipedrive_post(PIPEDRIVE_PERSON_URL, data=data)['data']['id']


	# also create a deal
	data = {
		'title': "Deal of " + email,
		'person_id': person_id,
		'stage_id': DEFAULT_STAGE_ID,
		'value': 2000,
		'currency': "EUR",
		'visible_to': 3,
		'user_id': USER_ID
	}
	deal_id = _pipedrive_post(PIPEDRIVE_DEAL_URL, data=data)['data']['id']


	return person_id


#
# Pipedrive helpers
#
def _pipedrive_get(url, params = {}):
	params['api_token'] = PIPEDRIVE_API_KEY
	return requests.get(url, params=params).json()


def _pipedrive_post(url, params = {}, data = {}):
	params['api_token'] = PIPEDRIVE_API_KEY
	result = requests.post(url, params=params, data=data)
	return result.json()