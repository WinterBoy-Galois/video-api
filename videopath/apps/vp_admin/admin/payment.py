from django.contrib import admin
from videopath.apps.payments.util import payment_export_util

from .base import VideopathModelAdmin

from ..models import  Payment

#
# Payents admin
#
class PaymentAdmin(VideopathModelAdmin):

	list_display = ('number', 'recipient', 'total', 'created', 'paid','provider', 'link', 'current_plan')
	ordering = ('-created',)
	search_fields = ['number', 'user__email', 'user__username']
	list_filter = ['paid', 'created']


	def recipient(self, obj):
		return obj.user.email
	recipient.admin_order_field = 'user__email'


	def total(self, obj):
		return '{0} {1}'.format(obj.amount_due/100, obj.currency)
	total.admin_order_field = 'amount_due'


	def link(self, payment):
		url = payment_export_util.url_for_payment(payment) 
		return "<a href = '%s'>View</a>" % url
	link.allow_tags = True

	#
	# List display
	#
	def current_plan(self, obj):
		try:
			plan = obj.user.subscription.plan
		except:
			return 'free-free'
		status = ''
		try:
			status = 'switches to {0} on {1}'.format(obj.user.pending_subscription.plan, obj.user.subscription.current_period_end)
		except: 	
			if obj.user.subscription.current_period_end:
				status = 'renews {0}'.format(obj.user.subscription.current_period_end)

		return "{0}<br />{1}".format(plan, status)
	current_plan.admin_order_field = 'user__subscription__plan'
	current_plan.allow_tags = True


	#
	#
	#
	def make_mark_as_paid(self, request, queryset):
	    for payment in queryset.all():
		    payment.paid = True
		    payment.save()

	make_mark_as_paid.short_description = "Mark as paid"
	actions=["make_mark_as_paid"]


admin.site.register(Payment, PaymentAdmin)