import json

from rest_framework import viewsets
from rest_framework.response import Response

from .util import oauth2_util

from .services import config
from .models import Integration

from videopath.apps.users.models import Team

#
# get object description of integration for one user
#
def get_integration_info(team, service):

    # get config of this service
    service_config = config.get(service, None)
    if not service_config:
        return {}

    # see if this config has been enabled
    try:
        integration = Integration.objects.get(team=team, service=service)
    except Integration.DoesNotExist:
        integration = None

    result = {
        'configured': False,
        'id': service,
        'title': service_config.get('title'),
        'oauth2_endpoint': oauth2_util.authorize_uri_for_team(service_config, team),
        'description': service_config.get('description'),
        'credentials': service_config.get('credentials', False),
        'type': service_config.get('type')
    }

    if integration:
        result['configured'] = True
        result['created'] = integration.created

    return result

#
# get list of integration infos for one user
#
def get_integration_list(team):
    results = []

    for service in config:
        results.append(get_integration_info(team, service))

    return {
        'count': len(results),
        'results': results,
        'next': None,
        'previous': None
    }

def authorize_with_credentials(team, service, credentials):
    service_config = config.get(service, None)
    credentials = service_config['module'].handle_credential_request(credentials)
    if credentials:
        credentials = json.dumps(credentials)
        Integration.objects.create(team=team, service=service, credentials=credentials)
        return True
    else:
        return False

#
# Manage the integrations for a user
#
class IntegrationViewSet(viewsets.ViewSet):

    def list(self, request, team_id=None):
        team = Team.objects.teams_for_user(request.user).distinct().get(pk=team_id)
        data = get_integration_list(team)
        return Response(data)

    # create is disabled
    def create(self, request):
        return Response({}, 404)

    #
    def retrieve(self, request, pk=None, team_id=None):
        team = Team.objects.teams_for_user(request.user).distinct().get(pk=team_id)
        data = get_integration_info(team, pk)
        return Response(data)

    def update(self, request, pk=None, team_id=None):

        # see if this is a request to authorize with credentials
        team = Team.objects.teams_for_user(request.user).distinct().get(pk=team_id)
        if authorize_with_credentials(team, pk, request.data.get('authorize', None)):
            return self.retrieve(request, pk)
        else:
            return Response(status=403)

    def partial_update(self, request, pk=None):
        return self.retrieve(request, pk)

    #
    # delete data associated with this users integration
    #
    def destroy(self, request, pk=None, team_id=None):
        try:
            team = Team.objects.teams_for_user(request.user).distinct().get(pk=team_id)
            integration = Integration.objects.get(team=team, service=pk)
            integration.delete()
        except Integration.DoesNotExist:
            pass
        data = get_integration_info(request.user.default_team, pk)
        return Response(data)

