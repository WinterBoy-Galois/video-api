
from videopath.apps.common.test_utils import BaseTestCase

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	# make sure that a settings object gets created when a user does
        self.assertIsNotNone(self.user.settings)