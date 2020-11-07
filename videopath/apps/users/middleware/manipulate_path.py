from rest_framework import exceptions

from videopath.apps.users.util import token_util

#
# Manipulate the users path
#
class ManipulatePathMiddleware(object):

    def process_request(self, request):

    	if "user/me" in request.path:

			# try to get user from request
			user = request.user if request.user.is_authenticated() else None

			if "HTTP_AUTHORIZATION" in request.META and not user:
				token_string = request.META["HTTP_AUTHORIZATION"].replace("Token ", "").strip()

				try:
					user, token = token_util.authenticate_token(token_string)
				except exceptions.AuthenticationFailed:
					pass
			
			if user:
				url = "user/" + str(user.pk)
				request.path = request.path.replace("user/me", url)
				request.path_info = request.path_info.replace("user/me", url)

