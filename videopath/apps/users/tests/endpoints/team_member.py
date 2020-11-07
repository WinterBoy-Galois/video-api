from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

from videopath.apps.users.models import Team, TeamMember

TEAM_URL = '/v1/team/'
TEAMMEMBER_NESTED_URL = '/v1/team/{0}/team-member/'
TEAMMEMBER_URL = '/v1/team-member/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

	def test_anonymous_access(self):
		self.setup_users_and_clients()

		response = self.client.get_json(TEAMMEMBER_URL)
		self.assertEqual(response.status_code, 403)

		response = self.client.get_json(TEAMMEMBER_NESTED_URL.format(self.user1.default_team.pk))
		self.assertEqual(response.status_code, 403)

	def test_adding_members(self):

		# adding members
		self.setup_users_and_clients(4)

		team = Team.objects.create(owner=self.user1)

		# user 1, the owner, can add members
		response = self.client_user1.post_json(TEAMMEMBER_NESTED_URL.format(team.pk), {'email': self.user2.email, 'team': team.pk})
		self.assertEqual(response.status_code, 201)

		# but not from unknown email addresses
		response = self.client_user1.post_json(TEAMMEMBER_NESTED_URL.format(team.pk), {'email': 'blah@gmx.net', 'team': team.pk})
		self.assertEqual(response.status_code, 404)

		# user 3 can't add members to this group
		response = self.client_user3.post_json(TEAMMEMBER_NESTED_URL.format(team.pk), {'email': self.user4.email, 'team': team.pk})
		self.assertEqual(response.status_code, 403)

		# after becoming and admin, he now can
		response = self.client_user1.post_json(TEAMMEMBER_NESTED_URL.format(team.pk), {'email': self.user3.email, 'team': team.pk, 'role': 'admin'})
		self.assertEqual(response.status_code, 201)

		response = self.client_user3.post_json(TEAMMEMBER_NESTED_URL.format(team.pk), {'email': self.user4.email, 'team': team.pk})
		self.assertEqual(response.status_code, 201)


	def test_listing_groups_as_members(self):
		self.setup_users_and_clients(4)

		team = Team.objects.create(owner=self.user1)

		# user 2 only has default team
		response = self.client_user2.get_json(TEAM_URL)
		self.assertEqual(response.data.get('count'), 1)

		# user 2 can now see two teams
		team.add_member(self.user2)
		response = self.client_user2.get_json(TEAM_URL)
		self.assertEqual(response.data.get('count'), 2)

		# user 3 can only see own team
		response = self.client_user3.get_json(TEAM_URL)
		self.assertEqual(response.data.get('count'), 1)


	def test_listing_all_members(self):
		self.setup_users_and_clients(2)

		# no memberships should be visible
		response = self.client_user1.get_json(TEAMMEMBER_URL)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.get('count'), 0)

	def test_listing_members_as_members(self):

		self.setup_users_and_clients(4)

		team = Team.objects.create(owner=self.user1)
		team.add_member(self.user2)
		team.add_member(self.user3, role='admin')

		# owner should be able to see list
		response = self.client_user1.get_json(TEAMMEMBER_NESTED_URL.format(team.pk))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.get('count'), 2)

		# other member should be able to see all members in this team
		response = self.client_user2.get_json(TEAMMEMBER_NESTED_URL.format(team.pk))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.get('count'), 2)

		# user not in this team should not have access
		response = self.client_user4.get_json(TEAMMEMBER_NESTED_URL.format(team.pk))
		self.assertEqual(response.data.get('count'), 0)




	def chaging_user_access_level(self):
		self.setup_users_and_clients(3)

		team = Team.objects.create(owner=self.user1)
		member = team.add_member(self.user2)

		response = self.client_user1.post_json(TEAMMEMBER_URL + str(member.pk), {'role':'admin'})
		self.assertEqual(response.status_code, 200)
		self.assertIsTrue(team.is_user_admin(self.user2))

		# other user can not access this
		response = self.client_user3.post_json(TEAMMEMBER_URL + str(member.pk), {'role':'editor'})
		self.assertEqual(response.status_code, 403)


