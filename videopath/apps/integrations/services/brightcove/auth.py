
import requests
from requests.auth import HTTPBasicAuth

ACCESS_TOKEN_URL = 'https://oauth.brightcove.com/v3/access_token'



def get_token(credentials):

	client_id = credentials.get('client_id')
	client_secret = credentials.get('client_secret')

	headers = {
		'content-type': 'application/x-www-form-urlencoded'
	}
	response = requests.post(ACCESS_TOKEN_URL, 
		auth=HTTPBasicAuth(client_id, client_secret), 
		headers=headers,
		data={'grant_type':'client_credentials'})

	try:
		return response.json().get('access_token')
	except:
		return None

def handle_credential_request(credentials): 
	
	list_videos(credentials)

	if get_token(credentials):
		return credentials
	else:
		return None

def list_videos(credentials):

	url = 'https://api.brightcove.com/services/library'

	params = {
		'command': 'search_videos',
		'page_size': '3',
		'video_fields': 'id,name,shortDescription',
		'token': get_token(credentials),
		'page_number':'0',
		'get_item_count': 'true'
	}
	response = requests.get(url, params=params)
	print response.json()


	