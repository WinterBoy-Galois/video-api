from django.test import TestCase

from videopath.apps.common.services import service_provider

# Uses the standard django frame testing client
class TestClass(TestCase):

    def setUp(self):
        # do some setup stuff
        self.service = service_provider.get_service("mail")
        self.assertIsNotNone(self.service)

    def test_something(self):
        # do some testing

        message = {
	        'subject': "Test Mail",
	        'text': "Test Message",
	        'to': [{'email': 'null@videopath.com'}],
	        'from_email': 'david@videopath.com',
	        'from_name': 'David',
	        'inline_css': True,
	        'tags': ['agent'],
	    }

        self.service.mandrill_send(message)
