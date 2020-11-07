
from django.http import HttpResponseRedirect

from services import config

from django.conf import settings

from .util import oauth2_util


# redirect urls
FAIL_URL = settings.APP_URL + '/#teams?integration_result=failure'

SUCCESS_TEAM_URL = settings.APP_URL + '/#team/{0}?integration_result=success'
FAIL_TEAM_URL = settings.APP_URL + '/#team/{0}?integration_result=failure'


#
# Receive oauth requests
#
def oauth_receive(request, service):

	# find service definition
	try:
		service_config = config[service]
	except:
		return HttpResponseRedirect(FAIL_URL)	

	success, team = oauth2_util.handle_redirect(request, service_config)
	if success:
		return HttpResponseRedirect(SUCCESS_TEAM_URL.format(team.pk))
	if team:
		return HttpResponseRedirect(FAIL_TEAM_URL.format(team.pk))
	return HttpResponseRedirect(FAIL_URL)

