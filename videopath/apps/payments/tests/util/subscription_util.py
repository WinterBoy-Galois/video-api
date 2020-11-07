from datetime import date
from dateutil.relativedelta import relativedelta

from videopath.apps.users.models import User

from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.payments.util import subscription_util
from videopath.apps.payments.models import Subscription, PendingSubscription, Payment, PaymentDetails


class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()
        PaymentDetails.objects.create(user=self.user, country="Germany")

    def test_subscribe_to_plan(self):

        # default plan should be the free plan
        self.assertEqual(subscription_util.get_currently_active_plan_for_user(
            self.user)["id"], "free-free")

        # test subscribing to free plan
        subscription_util.subscribe_user(self.user, "201509-starter-monthly")

        # we should now be subscribed to a plan
        self.assertEqual(self.user.subscription.plan, "201509-starter-monthly")
        self.assertEqual(self.user.subscription.currency, "EUR")

        # and there should be a payment
        self.assertEqual(self.user.payments.latest("number").amount_due, 7900)
        self.assertEqual(self.user.payments.latest("number").currency, "EUR")

    def test_subscribe_to_plan_with_payment_email(self):

        self.user.payment_details.email = 'dscharf@gmx.net'
        self.user.payment_details.save()

        # default plan should be the free plan
        self.assertEqual(subscription_util.get_currently_active_plan_for_user(
            self.user)["id"], "free-free")

        # test subscribing to free plan
        subscription_util.subscribe_user(self.user, "201509-starter-monthly")

        # we should now be subscribed to a plan
        self.assertEqual(self.user.subscription.plan, "201509-starter-monthly")
        self.assertEqual(self.user.subscription.currency, "EUR")

        # and there should be a payment
        self.assertEqual(self.user.payments.latest("number").amount_due, 7900)
        self.assertEqual(self.user.payments.latest("number").currency, "EUR")

    def test_remaining_credit(self):

        startdate = date.today() - relativedelta(days=10)
        Subscription.objects.create(
            user=self.user,
            plan="201412-starter-monthly",
            current_period_start=startdate,
            current_period_end=startdate + relativedelta(months=1),
            price=3500,
            managed_by=Subscription.MANAGER_SYSTEM
        )
        amount, line = subscription_util._get_remaining_credit_of_current_plan(
            self.user)
        self.assertAlmostEqual((2.0 / 3.0) * 3500, amount, delta=100)

    def test_unsubscribe_from_plan(self):
        subscription_util.subscribe_user(self.user, "201509-starter-monthly")
        subscription_util.subscribe_user(self.user, "free-free")
        # current plan should still be starter, but this should switch to free
        # soon
        self.assertEqual(self.user.pending_subscription.plan, "free-free")
        self.assertEqual(self.user.subscription.plan, "201509-starter-monthly")
        self.assertEqual(self.user.payments.latest("number").amount_due, 7900)

    def test_upgrading_subscription(self):

        subscription_util.subscribe_user(self.user, "201509-starter-monthly")
        subscription_util.subscribe_user(self.user, "201412-pro-plus-monthly")
        self.assertEqual(self.user.subscription.plan, "201412-pro-plus-monthly")

        # should be pro price minus monthly price
        self.assertEqual(self.user.payments.latest("number").amount_due, 27000)

    def test_plan_renewal(self):
        startdate = date.today() - relativedelta(months=10)
        Subscription.objects.create(
            user=self.user,
            plan="201509-starter-monthly",
            current_period_start=startdate,
            current_period_end=date.today(),
            price=3500,
            managed_by=Subscription.MANAGER_SYSTEM
        )
        subscription_util.update_subscriptions()

        # one payment should be created
        self.assertEqual(self.user.payments.latest("number").amount_due, 7900)

    def test_plan_auto_switching(self):
        startdate = date.today() - relativedelta(months=10)
        enddate = date.today() - relativedelta(days=10)
        Subscription.objects.create(
            user=self.user,
            plan="201412-starter-monthly",
            current_period_start=startdate,
            current_period_end=enddate,
            price=3500,
            managed_by=Subscription.MANAGER_SYSTEM
        )
        PendingSubscription.objects.create(user=self.user, plan="free-free")
        subscription_util.update_subscriptions()
        self.user = User.objects.get(pk = self.user.id)
        self.assertEqual(self.user.subscription.plan, "free-free")
        self.assertEqual(Payment.objects.count(), 0)

    def test_subscription_with_dollars(self):
        # switch user to usd
        self.user.settings.currency = "USD"
        self.user.settings.save()

        subscription_util.subscribe_user(self.user, "201509-starter-monthly")

        # subscription should be in USD
        self.assertEqual(self.user.subscription.currency, "USD")
        # payment should be in USD
        self.assertEqual(self.user.payments.latest("number").currency, "USD")








