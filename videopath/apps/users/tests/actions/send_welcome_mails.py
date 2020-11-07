from datetime import timedelta, datetime

from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.users.actions import send_welcome_mails

from videopath.apps.users.models import AutomatedMail, UserSalesInfo

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_send_regular(self):
    	
    	# a new user should not receive automails
        send_welcome_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),0)

        # a user that joined over a week ago should
        self.user.date_joined = datetime.today() - timedelta(days=9)
        self.user.save()
        send_welcome_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),1)

        # running the command again should not throw an error
        send_welcome_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),1)

    # welcome emails should not be sent to users which have a pipedrive account
    def test_send_if_in_pipedrive(self):
    	self.user.date_joined = datetime.today() - timedelta(days=9)
        self.user.save()
        UserSalesInfo.objects.create(user=self.user, pipedrive_person_id=234234)
        send_welcome_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),0)

    def test_send_if_retention_disabled(self):
        self.user.date_joined = datetime.today() - timedelta(days=9)
        self.user.save()
        self.user.settings.receive_retention_emails = False
        self.user.settings.save()
        send_welcome_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),0)
