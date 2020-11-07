from videopath.apps.payments.models import Subscription
from videopath.apps.payments.signals import subscription_updated

def run(user):
	try:
		user.pending_subscription.delete()
	except: pass
	user.subscription.delete()
	Subscription.objects.create(user=user)
	subscription_updated.send_robust(sender=user, user=user)