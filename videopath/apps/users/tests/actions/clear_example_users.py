from videopath.apps.common.test_utils import BaseTestCase

from videopath.apps.users.models import User

from videopath.apps.users.actions import clear_example_users

class TestCase(BaseTestCase):

    def test_run(self):
    	self.assertEqual(User.objects.count(), 1)
    	User.objects.create(email='dscharf@gmx.net', username='u1')
    	User.objects.create(email='dscharf@gmx.de', username='u2')
    	User.objects.create(email='user1@example.com', username='u3')
    	User.objects.create(email='user2@example.com', username='u4')
    	self.assertEqual(User.objects.count(), 5)
        clear_example_users.run()
        self.assertEqual(User.objects.count(), 3)