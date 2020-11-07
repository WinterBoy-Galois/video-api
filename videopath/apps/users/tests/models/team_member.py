
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.users.models import Team, TeamMember

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	t = Team.objects.create(owner=self.user)
    	TeamMember.objects.create(user=self.user1, team=t)