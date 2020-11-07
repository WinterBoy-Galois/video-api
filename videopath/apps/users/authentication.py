from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication

from videopath.apps.users.util import token_util

# override django rest framework auth to use our token
class TokenAuthentication(BaseTokenAuthentication):

    def authenticate_credentials(self, key):
        user, token = token_util.authenticate_token(key)
        return (user,token)
