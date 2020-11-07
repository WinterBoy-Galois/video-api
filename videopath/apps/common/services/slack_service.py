from slacker import Slacker
from django.conf import settings

def notify(text):
	try:
		slack = Slacker(settings.SLACK_API_TOCKEN)
		slack.chat.post_message('#product-activity', text, as_user=True)
	except:
		pass