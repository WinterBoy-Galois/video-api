
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.payments.models import Subscription

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	subs = Subscription.objects.create(user=self.user)
        self.assertIsNotNone(subs)