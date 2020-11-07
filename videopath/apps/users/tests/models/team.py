
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.users.models import Team

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	Team.objects.create(owner=self.user)

    def test_add_and_remove_members(self):
    	t = Team.objects.create(owner=self.user)

    	#check own state
    	self.assertEqual(t.is_user_member(self.user), True)
    	self.assertEqual(t.is_user_admin(self.user), True)
    	self.assertEqual(t.is_user_owner(self.user), True)

    	# add regular member
    	t.add_member(self.user2)
    	self.assertEqual(t.is_user_member(self.user2), True)
    	self.assertEqual(t.is_user_admin(self.user2), False)
    	self.assertEqual(t.is_user_owner(self.user2), False)

    	t.remove_member(self.user2)
    	self.assertEqual(t.is_user_member(self.user2), False)

    	# add admin
    	t.add_member(self.user2, role='admin')
    	self.assertEqual(t.is_user_member(self.user2), True)
    	self.assertEqual(t.is_user_admin(self.user2), True)
    	self.assertEqual(t.is_user_owner(self.user2), False)

