from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

from videopath.apps.integrations.models import Integration

INTEGRATION_URL = '/v1/team/{0}/integration/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_list_integrations(self):
        self.setup_users_and_clients()

        # should show a list of integrations
        response = self.client_user1.get_json(INTEGRATION_URL.format(self.user1.default_team.pk))
        self.assertTrue(len(response.data) >= 1)
        self.assertEqual(response.status_code, 200)

    def test_manipulate_integration(self):
		self.setup_users_and_clients()

		# unconfigured integration
		response = self.client_user1.get_json(INTEGRATION_URL.format(self.user1.default_team.pk) + 'mailchimp/')
		self.assertEqual(response.data.get('id'), 'mailchimp')
		self.assertEqual(response.data.get('configured'), False)
		self.assertEqual(response.status_code, 200)

		# create integration and see if the return is correct
		Integration.objects.create(team=self.user1.default_team, service='mailchimp')
		response = self.client_user1.get_json(INTEGRATION_URL.format(self.user1.default_team.pk) + 'mailchimp/')
		self.assertEqual(response.data.get('id'), 'mailchimp')
		self.assertEqual(response.data.get('configured'), True)

		# delete integration
		self.client_user1.delete_json(INTEGRATION_URL.format(self.user1.default_team.pk) + 'mailchimp/')
		response = self.client_user1.get_json(INTEGRATION_URL.format(self.user1.default_team.pk) + 'mailchimp/')
		self.assertEqual(response.data.get('configured'), False)