import mailchimp

from django.conf import settings


mc = mailchimp.Mailchimp(settings.MAILCHIMP_APIKEY)

#
# subscribe a user to our newsletter
#
def subscribe_email(email):
	mc.lists.subscribe("8d64e6c84e", {"email":email}, update_existing=True, double_optin=False)

#
# Test subscription
#
def check_access():
	try:
		subscribe_email("null@videopath.com")
		return True
	except Exception as e:
		return str(e)