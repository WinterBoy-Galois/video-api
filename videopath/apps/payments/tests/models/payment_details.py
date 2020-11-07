
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.payments.models import PaymentDetails

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	details = PaymentDetails.objects.create(user=self.user)
        self.assertIsNotNone(details)