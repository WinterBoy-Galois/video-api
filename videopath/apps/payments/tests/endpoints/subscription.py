from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

from videopath.apps.payments.models import Subscription, PendingSubscription, PaymentDetails, StripeID

SUBS_URL = '/v1/user/1/subscription/'
PLAN_ID = '201509-starter-monthly'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_get_and_post_access(self):
        self.setup_users_and_clients()

        # no subscription
        response = self.client_user1.get(SUBS_URL)
        self.assertEqual(response.status_code, 200)

        # should not work, as there is no credit card and no address involved
        response = self.client_user1.put_json(SUBS_URL, {"plan_id": PLAN_ID})
        self.assertEqual(response.status_code, 400)

        # simulate credit card and address
        PaymentDetails.objects.create(user=self.user1)
        StripeID.objects.create(user=self.user1, key="some key")

        # invalid plan id
        response = self.client_user1.put_json(SUBS_URL, {"plan_id":"some_plan"})
        self.assertEqual(response.status_code, 400)

        # with valid plan id it should work
        response = self.client_user1.put_json(SUBS_URL, {"plan_id":PLAN_ID})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(PendingSubscription.objects.count(), 0)

        # simulate unsubscribe
        response = self.client_user1.delete(SUBS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(PendingSubscription.objects.count(), 1)

