from datetime import date
from dateutil.relativedelta import relativedelta

from videopath.apps.users.models import User
from django.conf import settings

from videopath.apps.common import mailer
from videopath.apps.payments.util import payment_util
from videopath.apps.payments.models import Subscription, PendingSubscription

from videopath.apps.payments.signals import subscription_updated

#
# Subscribe the user to a plan
#
def subscribe_user(user, plan_id=None, coupon_id=None):

    # if plan is not valid, return false
    if settings.PLANS.get(plan_id, None) is None:
        return False, "Please specify a valid plan id."

    # get current state of users subscription
    subscription = None
    subscription, created = Subscription.objects.get_or_create(user=user, defaults={'managed_by': Subscription.MANAGER_SYSTEM, 'currency': user.settings.currency})
    if subscription.managed_by != Subscription.MANAGER_SYSTEM:
        return False, "Operation can't be performed at this time"

    # get plan info
    current_plan = settings.PLANS.get(subscription.plan, settings.DEFAULT_PLAN)
    target_plan = settings.PLANS.get(plan_id,settings.DEFAULT_PLAN)

    # always clear pending subscription
    try:
        user.pending_subscription.delete()
        user.save()
    except PendingSubscription.DoesNotExist:
        pass

    # if subscribing to the same plan, all is ok
    if plan_id == subscription.plan:
        return True, None

    # if subscribing to a more expensive plan, switch instantly
    if current_plan["value"] < target_plan["value"]:
        _update_plan_and_create_payment(user, plan_id)

    # if subscribing to a cheaper plan, add pending subscription
    if current_plan["value"] >= target_plan["value"]:
        PendingSubscription.objects.create(user=user, plan=plan_id)
        _send_email(user, "plan_will_change")

    return True, None

#
# Return current subscription for user
#
def subscription_for_user(user):
    try:
        return user.subscription
    except Subscription.DoesNotExist:
        subscribe_user(user, plan_id=settings.DEFAULT_PLAN["id"])
        return Subscription.objects.get(user=user)



#
# Unsubcribe the user
#
def unsubscribe_user(user):
    return subscribe_user(user, plan_id=settings.DEFAULT_PLAN["id"])

# 
# Get the plan the user is subscriped to
#
def get_currently_active_plan_for_user(user):
    try:
        if user.subscription.active:
            return settings.PLANS.get(user.subscription.plan, settings.DEFAULT_PLAN)
    except Subscription.DoesNotExist:
        pass
    return settings.DEFAULT_PLAN

#
# goes through all subs, and checks if changes need to be made
#
def update_subscriptions():
    for user in User.objects.all():
        _update_subscription_for_user(user)


#
# When use is switching a plan calculate the remaining credit
#
def _get_remaining_credit_of_current_plan(user):

    if user.subscription.current_period_end and user.subscription.current_period_end > date.today():

        # vars
        period_start = user.subscription.current_period_start
        period_end = user.subscription.current_period_end
        today = date.today()
        current_plan = settings.PLANS.get(user.subscription.plan, settings.DEFAULT_PLAN)

        # calculate amount
        base = (period_end - period_start).days
        used = (today - period_start).days
        amount = user.subscription.price - \
            int(float(used) / float(base) * user.subscription.price)

        # render payment line
        line = {
            "text": "Videopath " + current_plan["name"] + " " + str(period_start) + " until " + str(period_end) + " Refund",
            "amount": -amount
        }

        amount = amount if amount <= user.subscription.price else user.subscription.price
        return amount, line

    return 0, {}

#
#
#
def _set_subscription_to_plan(user, plan_id):

    # subscribe to the new pla
    target_plan = settings.PLANS.get(plan_id, settings.DEFAULT_PLAN)
    if target_plan["payment_interval"] == 'month':
        interval = relativedelta(months=1)
    elif target_plan["payment_interval"] == 'year':
        interval = relativedelta(years=1)
    else:
        raise

    # create new subscriptions object, or get existing
    subscription = user.subscription
    subscription.plan = plan_id
    subscription.current_period_start = date.today()
    subscription.current_period_end = date.today() + interval

    # determine currency & price
    subscription.currency = user.settings.currency
    price_id = settings.CURRENCY_SETTINGS[subscription.currency]['plan_string']
    subscription.price = target_plan[price_id]

    # save
    subscription.save()
    user.save()

    line = {
        "text": "Videopath " + target_plan["name"] + " " + str(subscription.current_period_start) + " until " + str(subscription.current_period_end),
        "amount": subscription.price
    }

    subscription_updated.send_robust(sender=user, user=user)

    return True, line

#
# Renew a subscription
#
def _renew_subscription(user):
    result, line = _set_subscription_to_plan(user, user.subscription.plan)
    payment_util.create_payment(user, [line], user.settings.currency)


#
# switch the plan and create a new payment from it
#
def _update_plan_and_create_payment(user, plan_id=None):
    current_plan = settings.PLANS.get(user.subscription.plan, settings.DEFAULT_PLAN)
    if not plan_id:
        plan_id = current_plan
    lines = []

    # get details about remaining credit of current subscription
    remaining_credit, line = _get_remaining_credit_of_current_plan(user)
    if remaining_credit > 0:
        lines.append(line)

    result, line = _set_subscription_to_plan(user, plan_id)

    lines.append(line)

    payment_util.create_payment(user, lines, user.settings.currency)

    # notify user
    _send_email(user, "plan_changed")



#
# update system subscription based on stripe and other parameters
#
def _update_subscription_for_user(user):
    try:
        if user.subscription.managed_by == Subscription.MANAGER_SYSTEM and user.subscription.current_period_end and user.subscription.current_period_end <= date.today():
            try:
                _update_plan_and_create_payment(user, user.pending_subscription.plan)
                user.pending_subscription.delete()
            except PendingSubscription.DoesNotExist:
                _renew_subscription(user)
    except Subscription.DoesNotExist:
        pass

#
# Send email to user, there are a couple of different actions
# plan_changed and plan_will_change
#
def _send_email(user, action=None):

    if action == "plan_changed":
        plan = settings.PLANS.get(user.subscription.plan, settings.DEFAULT_PLAN)
        mailer.send_mail('subscribe_change', {
                'plan':plan['name'], 
                'interval': plan["payment_interval"], 
                'is_free': plan.get("default", False)
                }, user)

    elif action == "plan_will_change":
        try:
            plan = settings.PLANS.get(user.pending_subscription.plan, settings.DEFAULT_PLAN)
            mailer.send_mail('subscribe_will_change', {
                    'plan': plan["name"],
                    'switch_date':user.subscription.current_period_end
                }, user)
        except PendingSubscription.DoesNotExist:
            pass
