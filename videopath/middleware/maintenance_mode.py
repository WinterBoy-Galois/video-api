from django import http

from django.conf import settings

#
# Make sure cross origin requests are accepted by the app
#
class MaintenanceModeMiddleware(object):

    def process_request(self, request):

    	#
    	#
    	#
        if settings.MAINTENANCE_IP:

        	#
        	# Extract client ip
        	#
			if 'HTTP_X_FORWARDED_FOR' in request.META:
				ip_adds = request.META['HTTP_X_FORWARDED_FOR'].split(",")   
				ip = ip_adds[0]
			else:
				ip = request.META['REMOTE_ADDR']
			print ip


			#
			# If IP does not match maintenance setting, catch request
			#
			if ip != settings.MAINTENANCE_IP:
				response = http.JsonResponse({'detail': 'Videopath API is currently in maintenance mode. Please try again in a few minutes.'}, status=503)
				return response


        return None
