from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from videopath.apps.common import health_checks

@api_view(['GET'])
@permission_classes((AllowAny,))
def view(request):
	result = health_checks.run()

	if result["failed"] == 0:
		return Response(result)
	else:
		return Response(result, status=500)