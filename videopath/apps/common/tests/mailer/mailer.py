from django.test import TestCase

from videopath.apps.common import mailer
from videopath.apps.common.mailer import conf

# Uses the standard django frame testing client
class TestClass(TestCase):

    def test_mail_rendering(self):

        for mail in conf.mails:
        	mailconf = mailer.prepare_mail(mail, {})

        	# assert basic info is there
        	self.assertIsNotNone(mailconf.get('subject'))
        	self.assertIsNotNone(mailconf.get('html'))
        	self.assertIsNotNone(mailconf.get('text'))
        	self.assertIsNotNone(mailconf.get('tags'))
        	self.assertIsNotNone(mailconf.get('from_email'))
        	self.assertIsNotNone(mailconf.get('from_name'))
        	self.assertIsNotNone(mailconf.get('replyto'))