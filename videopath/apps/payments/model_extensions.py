from videopath.apps.users.models import User
from videopath.apps.payments.util import subscription_util
from types import MethodType
from django.conf import settings

#
# Users User
#
def subscribe_to_plan(self, plan=None, coupon=None):
	return subscription_util.subscribe_user(self,plan,coupon)
User.subscribe_to_plan = MethodType(subscribe_to_plan, None, User)


def unsubscribe_from_plan(self):
	return subscription_util.unsubscribe_user(self)
User.unsubscribe_from_plan = MethodType(unsubscribe_from_plan, None, User)

def can_use_feature(self, feature):
	subscription = subscription_util.subscription_for_user(self)
	plan = settings.PLANS.get(subscription.plan, settings.DEFAULT_PLAN)
	feature = 'feature_' + feature
	return plan.get(feature, False)
User.can_use_feature = MethodType(can_use_feature, None, User)
