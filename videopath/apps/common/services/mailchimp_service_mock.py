import mailchimp

from django.conf import settings

mc = mailchimp.Mailchimp(settings.MAILCHIMP_APIKEY)

#
# subscribe a user to our newsletter
#
def subscribe_email(email):
	return True

#
# Test subscription
#
def check_access():
	return True