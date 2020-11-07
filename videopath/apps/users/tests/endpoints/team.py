from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

from videopath.apps.users.models import Team

TEAM_URL = '/v1/team/'
TEAMMEMBER_URL = '/v1/team/{1}/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

	def test_anonymous_access(self):
		self.setup_users_and_clients()
		response = self.client.get_json(TEAM_URL)
		self.assertEqual(response.status_code, 403)

	def test_ensure_default_team(self):
		self.setup_users_and_clients()
		response = self.client_user1.get_json(TEAM_URL)
		self.assertEqual(response.data.get('count'), 1)

	def test_create_team(self):
		
		self.setup_users_and_clients()
		response = self.client_user1.post_json(TEAM_URL, {'name': 'New Team'})
		self.assertEqual(response.status_code, 201)
		team_id = response.data.get('id')

		team = Team.objects.get(pk=team_id)
		self.assertEqual(team.is_user_owner(self.user1), True)

		# should now have default team and the new team
		self.assertEqual(self.user1.owned_teams.count(), 2)

	def test_access(self):
		self.setup_users_and_clients()

		t1 = Team.objects.create(owner=self.user1)
		t2 = Team.objects.create(owner=self.user2)

		response = self.client_user1.get_json(TEAM_URL + str(t1.pk) + '/')
		self.assertEqual(response.status_code, 200)

		response = self.client_user1.get_json(TEAM_URL + str(t2.pk) + '/')
		self.assertEqual(response.status_code, 404)

	def test_deleting(self):

		self.setup_users_and_clients()

		# can't delete default team
		response = self.client_user1.delete_json(TEAM_URL + str(self.user1.default_team.pk) + '/')
		self.assertEqual(response.status_code, 403)

		# can delete own team
		t1 = Team.objects.create(owner=self.user1)
		response = self.client_user1.delete_json(TEAM_URL + str(t1.pk) + '/')
		self.assertEqual(response.status_code, 204)

		# can't delete other team_id
		t1 = Team.objects.create(owner=self.user1)		
		response = self.client_user2.delete_json(TEAM_URL + str(t1.pk) + '/')
		self.assertEqual(response.status_code, 404)
