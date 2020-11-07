from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ValidationError

from videopath.apps.payments.models import PaymentDetails, Payment
from videopath.apps.payments.serializers import PaymentDetailsSerializer, PaymentSerializer, SubscriptionSerializer, CreditCardSerializer, PlanSerializer
from videopath.apps.payments.permissions import PaymentDetailsPermission
from videopath.apps.payments.util import subscription_util, payment_export_util
from videopath.apps.common.services import service_provider
from videopath.apps.common import serializers
from videopath.apps.common.views import SingletonViewSet


stripe_service = service_provider.get_service("stripe")


#
# Public view
#
def public_invoice(request, invoice_id):
    p = get_object_or_404(Payment,pk=invoice_id)
    s = payment_export_util.render_payment(p)
    return HttpResponse(s)


#
# Manage subscriptions
#
@api_view(['GET', 'PUT', 'DELETE'])
def subscription_view(request, uid=None):
    if uid != str(request.user.id):
        raise PermissionDenied

    # subscribe
    if request.method == "PUT":
        try:
            request.user.stripe_id
            request.user.payment_details
        except:
            raise ValidationError(detail="Please make sure you have a credit card and a valid address.")
        plan_id = request.data.get("plan_id", None)
        success, message = request.user.subscribe_to_plan(plan_id)

        if not success:
            raise ValidationError(detail=message)

    # unsubcribe
    if request.method == "DELETE":
        request.user.unsubscribe_from_plan()


    # return current subscription here
    subs = subscription_util.subscription_for_user(request.user)
    s = SubscriptionSerializer(subs)
    return Response(s.data)

    

#
# Get and set credit card (via stripe)
#
@api_view(['GET', 'PUT'])
def credit_card_view(request, uid=None, pk=None):
    if uid != str(request.user.id):
        raise PermissionDenied

    # save new card
    if request.method == "PUT":
        token = request.data.get("token",None)
        if not token:
            raise ValidationError(detail="Please specify a token!")
        success, message, card = stripe_service.set_card_for_user(request.user, token)
        if not success:
            raise ValidationError(detail=message)
        return Response(CreditCardSerializer(card).data)

    # get and return current card
    card = stripe_service.get_card_for_user(request.user)
    if card is None:
        raise Http404

    return Response(CreditCardSerializer(card).data)

#
# Get a list of all plans that are subscribable from the api
#
@api_view(['GET'])
def plan_view(request):
    name = request.GET.get('group', None)
    plans = settings.SUBSCRIBABLE_PLANS(name)
    serializer = serializers.get_paginated_serializer(plans, PlanSerializer, {"currency":request.user.settings.currency})
    return Response(serializer.data)


#
# Payment details / address, singleton
#
class PaymentDetailsViewSet(SingletonViewSet):

    model = PaymentDetails
    serializer_class = PaymentDetailsSerializer
    permission_classes = (PaymentDetailsPermission,)

    def get_singleton_object(self, request, uid=None):
        return PaymentDetails.objects.get(user_id=uid)

    def get_queryset(self, uid = None, pk=None):
        return PaymentDetails.objects.filter(user_id=uid)

    def perform_update_or_create(self, request, serializer, *args, **kwargs):
        serializer.save(user=request.user)
    


#
# Payments, a.k.a. invoices
#
class PaymentsViewSet(viewsets.ReadOnlyModelViewSet):

    model = Payment
    serializer_class = PaymentSerializer

    def get_queryset(self, uid=None):
        return Payment.objects.filter(user=self.request.user).order_by('-date')
