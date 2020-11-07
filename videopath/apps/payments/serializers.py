from rest_framework import serializers

from django.conf import settings

from videopath.apps.payments.models import PaymentDetails, Subscription, Payment, PendingSubscription
from videopath.apps.payments.util import payment_export_util, usage_util

#
# Serialize plans
#
class PlanSerializer(serializers.Serializer):

    # id
    id = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    group = serializers.CharField(max_length=200)

    # payment details
    payment_interval = serializers.CharField(max_length=200)

    price = serializers.SerializerMethodField()
    def get_price(self, plan):
        price_id = settings.CURRENCY_SETTINGS[self.user_currency]['plan_string']
        return plan[price_id]

    currency = serializers.SerializerMethodField()
    def get_currency(self,plan):
        return self.user_currency

    currency_symbol = serializers.SerializerMethodField()
    def get_currency_symbol(self,plan):
        return settings.CURRENCY_SETTINGS[self.user_currency]['symbol']

    # plan contraints
    max_views_month = serializers.IntegerField()
    max_projects = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        self.user_currency = kwargs.pop('currency', settings.CURRENCY_EUR)
        super(PlanSerializer, self).__init__(*args, **kwargs)

#
# Serialize CreditCards
#
class CreditCardSerializer(serializers.Serializer):

    last4 = serializers.CharField(max_length=200)
    exp_month = serializers.IntegerField()
    exp_year = serializers.IntegerField()

#
# Payment Details / Address
#
class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = ('name', 'street', 'city', 'post_code', 'country', 'vat_id')

#
# Payment / Invoices
#
class PaymentSerializer(serializers.ModelSerializer):

    download_url = serializers.SerializerMethodField()

    def get_download_url(self, payment):
        return payment_export_util.url_for_payment(payment)

    class Meta:
        model = Payment
        fields = ('amount_due', 'date', 'paid', 'number', 'download_url', 'currency')
        readonly_fields = ('amount_due', 'date', 'paid', 'number', 'currency')

#
# Actual subscription
#
class SubscriptionSerializer(serializers.ModelSerializer):

    plan = serializers.SerializerMethodField()

    pending_subscription = serializers.SerializerMethodField()

    current_month_views = serializers.SerializerMethodField()

    def get_current_month_views(self, subscription):
        return usage_util.plan_usage_current(subscription.user)

    def get_plan(self, subscription):
        plan = settings.PLANS.get(subscription.plan, settings.DEFAULT_PLAN)
        return PlanSerializer(plan, currency = subscription.currency).data

    def get_pending_subscription(self, subscription):
        try:
            plan = settings.PLANS.get(subscription.user.pending_subscription.plan, settings.DEFAULT_PLAN)
            return PlanSerializer(plan, currency = subscription.currency).data
        except PendingSubscription.DoesNotExist:
            return False


    class Meta:
        model = Subscription
        fields = ( 'current_period_start', 'current_period_end', 'current_month_views', 'plan', 'pending_subscription')
        read_only_fields = ( 'plan','current_period_start', 'current_period_end')
