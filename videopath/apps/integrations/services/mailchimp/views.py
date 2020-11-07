from rest_framework import viewsets

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import mailchimp

from videopath.apps.integrations.decorators import authenticate_service_viewset, authenticate_service_beacon

#
# Send list of available lists to user
#
class ListsViewSet(viewsets.ViewSet):
	@authenticate_service_viewset('mailchimp')
	def list(self, request, credentials):
		mc = mailchimp.Mailchimp(credentials['api_key'])
		result = mc.lists.list()

		results = map(lambda item: {'id': item['id'], 'title': item['name']}, result['data'] )

		return Response({
			'count': len(results),
	        'results': results,
	        'next': None,
	        'previous': None
			})

#
# beacon endpoint
#
@api_view(['GET'])
@permission_classes((AllowAny,))
@authenticate_service_beacon('mailchimp')
def beacon(request, credentials, owner):
	list_id = request.GET.get('list_id', 'f557548df1')
	email = request.GET.get('email', '')
	try:
		mc = mailchimp.Mailchimp(credentials['api_key'])
		mc.lists.subscribe(list_id, {"email":email}, update_existing=True)
	except Exception as e:
		pass
		# send to user
	return Response()


