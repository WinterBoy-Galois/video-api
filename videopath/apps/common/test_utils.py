from userena.models import UserenaSignup

from django.core.cache import cache

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from videopath.apps.users.models import AuthenticationToken, User

USER1_DETAILS = {
    "username": "dave",
    "password": "secret",
    "email": "null-1@videopath.com"
}

USER2_DETAILS = {
    "username": "dave2",
    "password": "secret2",
    "email": "null-2@videopath.com"
}

USER3_DETAILS = {
    "username": "dave3",
    "password": "secret3",
    "email": "null-3@videopath.com"
}

USER4_DETAILS = {
    "username": "dave4",
    "password": "secret4",
    "email": "null-4@videopath.com"
}

#
# util functions
#
def create_simple_user(username=USER1_DETAILS["username"], password = USER1_DETAILS["password"], email=USER1_DETAILS["email"]):
    permissions, users, warnings = UserenaSignup.objects.check_permissions()
    user = UserenaSignup.objects.create_user(username=username,
                                             password=password,
                                             email=email,
                                             active=True,
                                             send_email=False)
    return user

#
# Base client with some convenice functions
#
ip = "199.68.216.112" # us ip
class BaseAPIClient(APIClient):

    def post_json(self, url, data, **kwargs):
        return self.post(url, data, format='json', **kwargs)

    def put_json(self, url, data, **kwargs):
        return self.put(url, data, format='json', **kwargs)

    def get_json(self, url, **kwargs):
        return self.get(url, format='json', **kwargs)

    def delete_json(self, url, **kwargs):
        return self.delete(url, format='json', **kwargs)


#
# Base test class
#
class BaseTestCase(APITestCase):

    USER1_DETAILS = USER1_DETAILS
    USER2_DETAILS = USER2_DETAILS

    def setUp(self):

        # clear cache
        cache.clear()

        #run users setup routine
    	self.setup()

    def setup(self):
        pass

    #
    # Setup Test Users
    #
    def setup_users(self, num=2):
        self.user = create_simple_user(username=USER1_DETAILS["username"], password = USER1_DETAILS["password"], email=USER1_DETAILS["email"])
        self.user1 = self.user
        if num < 2: return
        self.user2 = create_simple_user(username=USER2_DETAILS["username"], password = USER2_DETAILS["password"], email=USER2_DETAILS["email"])
        if num < 3: return
        self.user3 = create_simple_user(username=USER3_DETAILS["username"], password = USER3_DETAILS["password"], email=USER3_DETAILS["email"])
        if num < 4: return
        self.user4 = create_simple_user(username=USER4_DETAILS["username"], password = USER4_DETAILS["password"], email=USER4_DETAILS["email"])

    #
    # Setup users and test api clients
    #
    def setup_users_and_clients(self, num=2):
        self.setup_users(num)

        # anonymous client
        self.client = BaseAPIClient()

        # user 1 client, authenticate with token
        self.client_user1 = BaseAPIClient()
        token = AuthenticationToken.objects.create(user=self.user1)
        self.client_user1.credentials( HTTP_AUTHORIZATION='Token %s' % token.key)
        if num < 2: return

        # user 2 client, authenticate with token
        self.client_user2 = BaseAPIClient()
        token = AuthenticationToken.objects.create(user=self.user2)
        self.client_user2.credentials( HTTP_AUTHORIZATION='Token %s' % token.key)
        if num < 3: return

        # user 3 client, authenticate with token
        self.client_user3 = BaseAPIClient()
        token = AuthenticationToken.objects.create(user=self.user3)
        self.client_user3.credentials( HTTP_AUTHORIZATION='Token %s' % token.key)
        if num < 4: return

        # user 4 client, authenticate with token
        self.client_user4 = BaseAPIClient()
        token = AuthenticationToken.objects.create(user=self.user4)
        self.client_user4.credentials( HTTP_AUTHORIZATION='Token %s' % token.key)


    # deprecated
    def create_user(self):
        self.setup_users()

    # deprecated
    def login_client(self):
        self.setup_users_and_clients()




