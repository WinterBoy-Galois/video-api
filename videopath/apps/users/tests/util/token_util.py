from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.users.models import AuthenticationToken, UserActivity, UserActivityDay
from videopath.apps.users.util import token_util

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_activity_tracking(self):
    	
    	# a new user should not receive automails
        token = AuthenticationToken.objects.create(user=self.user)
        token_util.authenticate_token(token.key)

        self.assertEqual(UserActivity.objects.count(),1)
        self.assertEqual(UserActivityDay.objects.count(),1)
