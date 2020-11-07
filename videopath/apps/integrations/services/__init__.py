
from django.conf import settings

from .mailchimp import auth as mailchimp
from .brightcove import auth as brightcove
from .vimeo import auth as vimeo

config = {

	'mailchimp': {
		'id': 'mailchimp',
		'title': 'Mailchimp',
		'description': 'Use Mailchimp to capture your viewers email addresses.',
		'type': 'email-collector',
		'module': mailchimp,
		'oauth2': {
			'client_id': settings.MAILCHIMP_CLIENT_ID,
			'client_secret': settings.MAILCHIMP_CLIENT_SECRET,
			'authorize_url': 'https://login.mailchimp.com/oauth2/authorize',
			'token_url': 'https://login.mailchimp.com/oauth2/token',
			'metadata_url': 'https://login.mailchimp.com/oauth2/metadata',
			'redirect_url': settings.API_ENDPOINT + '/oauth/receive/mailchimp/'
		}
	},

	
	# 'vimeo': {
	# 	'id': 'vimeo',
	# 	'title': 'Vimeo',
	# 	'description': 'Use Vimeo to host your videos',
	# 	'type': 'video-source',
	# 	'module': brightcove,
	# 	'oauth2': {
	# 		'client_id': settings.VIMEO_CLIENT_ID,
	# 		'client_secret': settings.VIMEO_CLIENT_SECRET,
	# 		'authorize_url': 'https://api.vimeo.com/oauth/authorize',
	# 		'token_url': 'https://api.vimeo.com/oauth/access_token',
	# 		'scope': 'private',
	# 		'redirect_url': settings.API_ENDPOINT + '/oauth/receive/vimeo/'
	# 	}
	# },

	# 'brightcove': {
	# 	'id': 'brightcove',
	# 	'title': 'Brightcove',
	# 	'description': 'Use Brightcove to host your videos',
	# 	'type': 'video-source',
	# 	'credentials': [{
	# 			'name': 'Brightcove Client ID',
	# 			'id': 'client_id'
	# 		}, {
	# 			'name': 'Brightcove Client Secret',
	# 			'id': 'client_secret'
	# 		}
	# 	],
	# 	'module': vimeo
	# },
	
}