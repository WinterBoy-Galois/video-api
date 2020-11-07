from videopath.apps.videos.tests.endpoints.endpoints_base import EndpointsBaseTestCase

from videopath.apps.videos.models import Video
from videopath.apps.integrations.models import Integration

MAILCHIMP_BEACON_URL = '/v1/beacon/mailchimp/'

# Uses the standard django frame testing client
class TestCase(EndpointsBaseTestCase):

    def test_mailchimp_beacon(self):
        self.setup_users_and_clients()

        # no params should not work
        response = self.client.get_json(MAILCHIMP_BEACON_URL)
        self.assertEqual(response.status_code, 404)

        # posting to existing video should work
        Integration.objects.create(service='mailchimp', team=self.user1.default_team, credentials='{"api_key": "something-else"}')
        v = Video.objects.create(team=self.user1.default_team)
        url = MAILCHIMP_BEACON_URL + '?video_key={0}'.format(v.key)
        response = self.client.get_json(url)
        self.assertEqual(response.status_code, 200)

