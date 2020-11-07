
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.users.models import AutomatedMail

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	mail = AutomatedMail.objects.create(user=self.user)
        self.assertIsNotNone(mail)