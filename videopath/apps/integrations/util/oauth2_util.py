import urllib, hashlib

import json

from datetime import date

from ..models import Integration
from videopath.apps.users.models import Team


def hash_team(team):
	return hashlib.sha224(str(team.owner.pk) + team.owner.email + str(date.today)).hexdigest()

def authorize_uri_for_team(service, team):

	if not 'oauth2' in service:
		return ''

	params = {
		'redirect_uri': service['oauth2']['redirect_url'],
		'client_id': service['oauth2']['client_id'],
		'response_type': 'code',
		'state': str(team.pk) + ' ' + hash_team(team)
	}

	if 'scope' in service['oauth2']:
		params['scope'] = service['oauth2'].get('scope')

	return service['oauth2']['authorize_url'] + '?' + urllib.urlencode(params)


def handle_redirect(request, service):

	state = request.GET.get('state','')
	code = request.GET.get('code','')
	team = None

	# try to load user
	try:
		tid = int(state.split(' ')[0])
		thash = state.split(' ')[1]
		team = Team.objects.get(pk=tid)
		# check hash
		if thash != hash_team(team):
			return False, team
	except Team.DoesNotExist:
		return False, team

	# try to handle oauth in service module
	credentials = service['module'].handle_redirect(service, team, code)
	if credentials:
		try:
			integration = Integration.objects.get(team=team, service=service)
			integration.delete()
		except Integration.DoesNotExist:
			pass
		credentials = json.dumps(credentials)
		integration = Integration.objects.create(team=team, service=service['id'], credentials=credentials)

		return True, team

	return False, team