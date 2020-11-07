from videopath.apps.users.authentication import TokenAuthentication

class TokenAuthMiddleware(object):

    #
    # 
    #
    def token_authenticate(self, request):
        authenticator = TokenAuthentication()
        user = None
        try:
            user = authenticator.authenticate(request)
            return user[0], user[1]
        except:
            return None, None