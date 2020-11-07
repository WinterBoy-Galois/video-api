from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

from videopath.apps.payments.models import Payment

INVOICE_URL = '/v1/user/1/invoice/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_get_and_post_access(self):
        self.setup_users_and_clients()

        Payment.objects.create(user=self.user1, exported_invoice=True)
        Payment.objects.create(user=self.user2, exported_invoice=True)

        response = self.client_user1.get(INVOICE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), 1)

        # posting should not be allowed
        response = self.client_user1.post_json(INVOICE_URL, {})
        self.assertEqual(response.status_code, 405)

