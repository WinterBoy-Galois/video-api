FREE_PLAN = 'free-free'
EVALUATION_PLAN = 'individual-agency-evaluation'
EVALUATION_PERIOD_WEEKS = 2

from videopath.apps.payments.models import PendingSubscription
from datetime import date, timedelta
from videopath.apps.payments.signals import subscription_updated

def run(user, weeks=EVALUATION_PERIOD_WEEKS):
	if user.subscription.plan != FREE_PLAN and user.subscription.plan != EVALUATION_PLAN:
		return False 
	
	user.subscription.plan = EVALUATION_PLAN
	user.subscription.current_period_start = date.today()
	user.subscription.current_period_end = date.today() + timedelta(weeks=EVALUATION_PERIOD_WEEKS)
	user.subscription.save()

	PendingSubscription.objects.create(user=user, plan=FREE_PLAN)
	subscription_updated.send_robust(sender=user, user=user)
	return True

