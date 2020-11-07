from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from videopath.apps.helpers.util import url_checker

@api_view(['GET'])
@permission_classes((AllowAny,))
def check_url_view(request):

	url = request.GET.get('url', '')
	cache_key = 'urlcheck-' + url
	result = cache.get(cache_key)
	
	if not result:
		result = url_checker.check_url(url)

	cache.set(cache_key, result, 60 * 10)

	return Response(result)