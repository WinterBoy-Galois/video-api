from django.contrib import admin

from videopath.apps.payments.models import Subscription, PaymentDetails, StripeID, QuotaInformation, Payment, PendingSubscription
from videopath.apps.payments.util import payment_export_util

class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'key')
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'paid', 'amount_due', 'number', 'download_url')
    def download_url(self, payment):
    	url = payment_export_util.url_for_payment(payment) 
    	return "<a href = '%s'>View</a>" % url
    download_url.allow_tags = True
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }


class QuotaInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'quota_exceeded', 'warning_sent')
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }


class StripeIDAdmin(admin.ModelAdmin):
    list_display = ('user', 'key')
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }


class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ('user',)
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'notes', 'active')
    search_fields = ['user__username', 'user__email']
    list_filter = ['plan', 'managed_by']
    
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }


class PendingSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan')
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }


admin.site.register(PaymentDetails, PaymentDetailsAdmin)
admin.site.register(Subscription, SubscriptionsAdmin)
admin.site.register(StripeID, StripeIDAdmin)
admin.site.register(QuotaInformation, QuotaInformationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PendingSubscription, PendingSubscriptionAdmin)
