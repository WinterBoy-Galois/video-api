import requests
from urlparse import urlparse

def _check_url(url, secure=False):
	try:
		parsed = urlparse(url)
		url = ('https://' if secure else 'http://') + parsed.netloc + parsed.path
		result = requests.head( url, allow_redirects=True, timeout=5,verify=False)
		if result.status_code == 405 or result.status_code == 403:
			result = requests.get( url, allow_redirects=True, timeout=5, verify=False)

		return {
			'reachable': result.status_code >= 200 and result.status_code < 300,
			'embedable': 'X-Frame-Options' not in result.headers
		}
	except requests.exceptions.RequestException:
		return {
			'reachable': False,
			'embedable': False
		}

def check_url(url):
	return {
		'url': url,
		'http': _check_url(url, False),
		'https': _check_url(url, True),
	}

