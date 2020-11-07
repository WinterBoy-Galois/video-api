from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

from videopath.apps.payments.models import PaymentDetails

ADDRESS_URL = '/v1/user/1/address/'

test_data = {
    'name': "Dave",
    'street': "Street",
    'city': "City",
    'post_code': "Post Code",
    'country': "Germany"
}

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_get_and_post_access(self):
        self.setup_users_and_clients()

        response = self.client_user1.get(ADDRESS_URL)
        self.assertEqual(response.status_code, 404)

        # test post
        response = self.client_user1.post_json(ADDRESS_URL, test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PaymentDetails.objects.count(), 1)

        # test get
        # should now succeed
        response = self.client_user1.get(ADDRESS_URL)
        self.assertEqual(response.status_code, 200)

        # not for user2 though
        response = self.client_user2.get(ADDRESS_URL)
        self.assertEqual(response.status_code, 403)




