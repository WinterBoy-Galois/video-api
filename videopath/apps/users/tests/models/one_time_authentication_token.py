
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.users.models import AuthenticationToken, OneTimeAuthenticationToken

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	token = AuthenticationToken.objects.create(user=self.user)
    	ottoken = OneTimeAuthenticationToken.objects.create(token=token)
        self.assertIsNotNone(ottoken)