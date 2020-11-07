import requests
from requests.auth import HTTPBasicAuth


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
		'code': code,
		'redirect_uri': service['oauth2']['redirect_url']
	}
	auth=HTTPBasicAuth(service['oauth2']['client_id'], service['oauth2']['client_secret'])
	response = requests.post(service['oauth2']['token_url'], headers = headers, data=data, auth=auth)
	token = response.json().get('access_token', '')

	if not token:
		return False

	return {
		'token': token
	}