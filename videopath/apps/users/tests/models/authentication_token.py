
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.users.models import AuthenticationToken

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	token = AuthenticationToken.objects.create(user=self.user)
        self.assertIsNotNone(token)