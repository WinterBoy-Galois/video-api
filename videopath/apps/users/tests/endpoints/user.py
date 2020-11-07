from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

USER_URL = '/v1/user/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_get_access(self):
        self.setup_users_and_clients()

        # should get list with one user
        response = self.client_user1.get_json(USER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), 1)

        # should be able to access myself
        response = self.client_user1.get_json(USER_URL + "1/")
        self.assertEqual(response.status_code, 200)

        # should not be able to access other user
        response = self.client_user1.get_json(USER_URL + "2/")
        self.assertEqual(response.status_code, 404)

    def test_change_email(self):
        self.setup_users_and_clients()

        new_email = "other@email.com"
        password = self.USER1_DETAILS["password"]

        # should not work, because a password is needed for the change
        response = self.client_user1.put_json(USER_URL + "me/", {"email":new_email})
        self.assertEqual(response.status_code,403)

        # should not work, as the email is malformed
        response = self.client_user1.put_json(USER_URL + "me/", {"email":"malformed email", "password":password})
        self.assertEqual(response.status_code,400)

        # should work
        response = self.client_user1.put_json(USER_URL + "me/", {"email":new_email, "password":password})
        self.assertEqual(response.status_code,200)

        user = self.user1.__class__.objects.get(pk=self.user1.pk)
        self.assertEqual(user.email, "other@email.com" )

    def test_change_password(self):
    	self.setup_users_and_clients()
        
        new_password = "password2"
        password = self.USER1_DETAILS["password"]

        # should not work, because a password is needed for the change
        response = self.client_user1.put_json(USER_URL + "1/", {"new_password":new_password})
        self.assertEqual(response.status_code,403)

        # should not work, as the email is to short
        response = self.client_user1.put_json(USER_URL + "1/", {"new_password":"short", "password":password})
        self.assertEqual(response.status_code,400)

        # should work
        response = self.client_user1.put_json(USER_URL + "1/", {"new_password":new_password, "password":password})
        self.assertEqual(response.status_code,200)

        user = self.user1.__class__.objects.get(pk=self.user1.pk)
        self.assertEqual(user.check_password(new_password), True)


    def test_signup(self):
        self.setup_users_and_clients()

        data = {
            'username': 'dave', 
            'password': 'pw'
        }

        # not enough data provided
        response = self.client.post_json(USER_URL, data)
        self.assertEqual(response.status_code, 400)

        # pw too short
        data = {
                'username': 'dave_new', 
                'password': 'short',
                'email': 'null@videopath.com'
        }
        response = self.client.post_json(USER_URL, data)
        self.assertEqual(response.status_code, 400)

        # invalid email
        data = {
            'username': 'dave_new', 
            'password': 'long_passsword',
            'email': 'nullvideopath.com'
        }
        response = self.client.post_json(USER_URL, data)
        self.assertEqual(response.status_code, 400)

        # taken username
        data = {
            'username': 'dave', 
            'password': 'long_passsword',
            'email': 'null@videopath.com'
        }
        response = self.client.post_json(USER_URL, data)
        self.assertEqual(response.status_code, 400)

        # taken email
        data = {
            'username': 'dave_new', 
            'password': 'long_passsword',
            'email': 'null-1@videopath.com'
        }
        response = self.client.post_json(USER_URL, data)
        self.assertEqual(response.status_code, 400)

        # should pass
        data = {
            'username': 'dave_new', 
            'password': 'long_passsword',
            'email': 'null@videopath.com'
        }
        response = self.client.post_json(USER_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("username"), "dave_new")

        # now check that signin works
        login = self.client.login(username="dave_new", password="long_passsword")
        self.assertEqual(login, True)


        # test very long username etc:
        data = {
            'username': 'newer_dave-superlongsuperlongsuperlongsuperlong',
            'password': '0i1029i3poljlsajfdoiajwef',
            'email': 'superlongandsuperduperlongblablabalablemail@blah.com'
        }
        response = self.client.post_json(USER_URL, data)
        self.assertEqual(response.status_code, 201)

    def test_currency_selection(self):
        from videopath.apps.users.models import User

        #
        # test if user with us ip address will be switched to USD
        #
        self.setup_users_and_clients()
        data = {
            'username': 'dave_new', 
            'password': 'long_passsword',
            'email': 'null-4@videopath.com'
        }
        ip = "199.68.216.112" # us ip
        self.client.post_json(USER_URL, data, HTTP_X_FORWARDED_FOR=ip)
        user = User.objects.get(username='dave_new')
        self.assertEqual(user.settings.currency, "USD")

        #
        # test if user with german ip address will be switched to USD
        #
        data = {
            'username': 'dave_new_2', 
            'password': 'long_passsword',
            'email': 'null-5@videopath.com'
        }
        ip = "84.159.212.138" # german ip
        self.client.post_json(USER_URL, data, HTTP_X_FORWARDED_FOR=ip)
        user = User.objects.get(username='dave_new_2')
        self.assertEqual(user.settings.currency, "EUR")


        #
        # test if user with uk ip address will be switched to GBP
        #
        data = {
            'username': 'dave_new_3', 
            'password': 'long_passsword',
            'email': 'null-6@videopath.com'
        }
        ip = "212.58.244.20" # british ip
        self.client.post_json(USER_URL, data, HTTP_X_FORWARDED_FOR=ip)
        user = User.objects.get(username='dave_new_3')
        self.assertEqual(user.settings.currency, "GBP")


    def test_campaign_data(self):
        from videopath.apps.users.models import User
        self.setup_users_and_clients()
        data = {
            'username': 'dave_new', 
            'password': 'long_passsword',
            'email': 'null-4@videopath.com',
            'referrer': 'videopath.com',
            'campaign': {
                'source':'source',
                'name':'name',
                'medium': 'medium'
            }
        }
        ip = "84.159.212.138" # german ip
        response = self.client.post_json(USER_URL, data, HTTP_X_FORWARDED_FOR=ip)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='dave_new')
        self.assertEqual(user.campaign_data.source,'source')
        self.assertEqual(user.campaign_data.medium,'medium')
        self.assertEqual(user.campaign_data.name,'name')
        self.assertEqual(user.campaign_data.referrer,'videopath.com')
        self.assertEqual(user.campaign_data.country,'Germany')

    def test_phone(self):
        from videopath.apps.users.models import User
        self.setup_users_and_clients()
        data = {
            'username': 'dave_new', 
            'password': 'long_passsword',
            'email': 'null-4@videopath.com',
            'phone': '1234567890',
        }
        response = self.client.post_json(USER_URL, data)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='dave_new')
        self.assertEqual(user.settings.phone_number, '1234567890')









