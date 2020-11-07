import json

from datetime import date

from django.conf import settings

from videopath.apps.common import mailer
from videopath.apps.payments.models import Payment, PaymentDetails
from videopath.apps.payments.util import payment_export_util
from videopath.apps.common.services import service_provider

stripe_service = service_provider.get_service("stripe")

#
# Create a new payment from a lines object
#
def create_payment(user, lines, currency):
    amount_due = 0
    percent_vat = 19

    # get correct vat
    try:
        country = user.payment_details.country
        if country in settings.VAT_RATES:
            percent_vat = settings.VAT_RATES[country]
        else:
            percent_vat = 0
    except PaymentDetails.DoesNotExist:
        pass

    # sum up
    for line in lines:
        amount_due += line["amount"]

    # if nothing is due, leave
    if amount_due <= 0:
        return

    payment = Payment.objects.create(
        user=user,
        date=date.today(),
        amount_due=amount_due,
        percent_vat=percent_vat,
        currency = currency,
        details=json.dumps(lines),
        provider=user.settings.payment_provider
    )
    url = payment_export_util.url_for_payment(payment)
    receiver = user.payment_details.email if user.payment_details.email else None
    mailer.send_mail('invoice_created', {'amount_due':amount_due, 'link': url, 'currency':currency}, payment.user, receiver)
    return payment

#
# Go through all payments and try to charge unpayed payments
#
def process_payments():

    # cycle all unpaid payments
    for payment in Payment.objects.filter(paid=False, provider=settings.PAYMENT_PROVIDER_STRIPE):

        # update charging attempt
        if payment.last_charging_attempt == None or payment.last_charging_attempt < date.today():
            payment.last_charging_attempt = date.today()
            # try charging
            provider, transaction_id = _charge_payment(payment)
            if provider:
                payment.provider = provider
                payment.transaction_id = transaction_id
                payment.paid = True
                payment.save()
                payment_export_util.export_payment(payment)
            else:
                # notify admin
                receiver = payment.user.payment_details.email if payment.user.payment_details.email else None
                mailer.send_mail('payment_failed', {'amount_due':payment.amount_due, 'currency':payment.currency}, payment.user, receiver)

            # save changes
            payment.charging_attempts += 1
            payment.save()

#
# Try to collect the money for a payment
#
def _charge_payment(payment):

    # try stripe
    charge_id = stripe_service.charge_user(payment.user, payment.amount_due, payment.currency)
    if charge_id:
        return settings.PAYMENT_PROVIDER_STRIPE, charge_id
    return None, None
   
