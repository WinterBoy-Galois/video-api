
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.users.models import UserActivity

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	activiy = UserActivity.objects.create(user=self.user)
        self.assertIsNotNone(activiy)