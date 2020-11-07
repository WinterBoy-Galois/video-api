import requests
from urlparse import urlparse

url = 'zeit.de'


def checkURL(url, secure=False):
	try:
		parsed = urlparse(url)
		url = ('https://' if secure else 'http://') + parsed.netloc + parsed.path
		result = requests.head( url, allow_redirects=True, timeout=5)
		if result.status_code == 405 or result.status_code == 403:
			result = requests.get( url, allow_redirects=True, timeout=5)

		return {
			'reachable': result.status_code >= 200 and result.status_code < 300,
			'embedable': 'X-Frame-Options' not in result.headers
		}
	except requests.exceptions.RequestException:
		return {
			'reachable': False,
			'embedable': False
		}

result = {
	'url': url,
	'http': checkURL(url, False),
	'https': checkURL(url, True),
}

print result