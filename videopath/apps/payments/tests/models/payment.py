
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.payments.models import Payment

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	payment = Payment.objects.create(user=self.user)
        self.assertIsNotNone(payment)