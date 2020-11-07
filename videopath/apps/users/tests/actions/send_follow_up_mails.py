from datetime import timedelta, datetime

from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.users.actions import send_follow_up_mails

from videopath.apps.users.models import AutomatedMail, UserActivity

four_weeks_ago = datetime.today() - timedelta(days=28)
seven_weeks_ago = datetime.today() - timedelta(days=49)

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_send_follow_up_mails(self):
    	
    	# a new user should not receive automails
        send_follow_up_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),0)

        # a user that joined over a week ago should
        UserActivity.objects.create(user=self.user, last_seen=four_weeks_ago)
        send_follow_up_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),1)

        # running the command again should not throw an error or send another mail
        send_follow_up_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),1)

        # fast forwarding should then send second follow up
        self.user.activity.last_seen = seven_weeks_ago
        self.user.activity.save()

        first_mail = AutomatedMail.objects.get(user=self.user)
        first_mail.created = four_weeks_ago
        first_mail.save()


        send_follow_up_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),2)

        # running the command again should not throw an error or send another mail
        send_follow_up_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),2)


    def test_send_follow_up_legacy(self):

    	# test should not send two mails in a row
        UserActivity.objects.create(user=self.user, last_seen=seven_weeks_ago)
        send_follow_up_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),1)

        # after putting mail in the past, this should work
        first_mail = AutomatedMail.objects.get(user=self.user)
        first_mail.created = four_weeks_ago
        first_mail.save()

        send_follow_up_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),2)

    def test_send_follow_up_retention_disabled(self):
        # a new user should not receive automails
        send_follow_up_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),0)

        # a user that joined over a week ago should
        UserActivity.objects.create(user=self.user, last_seen=four_weeks_ago)
        self.user.settings.receive_retention_emails = False
        self.user.settings.save()
        send_follow_up_mails.run()
        self.assertEqual(AutomatedMail.objects.count(),0)
