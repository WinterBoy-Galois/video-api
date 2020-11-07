import requests
from django.conf import settings



#
# handling incoming oauth request
#
def handle_redirect(service, team, code):

	# convert the code into an access token
	headers = {
		'content-type': 'application/x-www-form-urlencoded'
	}
	data = {
		'grant_type': 'authorization_code',
		'client_id': settings.MAILCHIMP_CLIENT_ID,
		'client_secret': settings.MAILCHIMP_CLIENT_SECRET,
		'code': code,
		'redirect_uri': service['oauth2']['redirect_url']
	}

	response = requests.post(service['oauth2']['token_url'], headers = headers, data=data)
	token = response.json().get('access_token', '')

	if not token:
		return False

	# complete the token to an api_key by getting the metadata for the datacenter
	headers = {
		'Authorization': 'OAuth ' + token,
		'Accept': 'application/json'
	}
	response = requests.get(service['oauth2']['metadata_url'], headers = headers)
	datacenter = response.json().get('dc', None)
	api_key = token + '-' + datacenter	

	# list our projects
	return {
		'api_key': api_key
	}