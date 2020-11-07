from django.conf.urls import url, patterns, include

from rest_framework import routers

from videopath.apps.payments.views import PaymentDetailsViewSet, PaymentsViewSet

router = routers.DefaultRouter()
router.register(r'user/(?P<uid>[0-9]+)/address', PaymentDetailsViewSet, base_name="address")
router.register(r'user/(?P<uid>[0-9]+)/invoice', PaymentsViewSet, base_name="invoice")

urlpatterns = patterns('',

   # list plans
   url(r'^plan/', 'videopath.apps.payments.views.plan_view'),

   # handle subscriptions
   url(r'^user/(?P<uid>[0-9]+)/subscription/', 'videopath.apps.payments.views.subscription_view'),

   # update and get users credit card
   url(r'^user/(?P<uid>[0-9]+)/credit-card/', 'videopath.apps.payments.views.credit_card_view'),

   # payment details, sort of allright...
   url(r'', include(router.urls)),

)
