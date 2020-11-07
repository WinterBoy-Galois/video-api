import json

from videopath.apps.common.services import service_provider

from django.template import Context
from django.template.loader import get_template
from django.conf import settings

#
# Export payment to rendered template and upload to s3
#
def export_payment(payment):

    s = render_payment(payment)

    key_id = _key_for_payment(payment)

    # save to s3
    s3_service = service_provider.get_service("s3")
    s3_service.upload(s, settings.AWS_DOCS_BUCKET, key_id, content_type="text/html", public=True)

    # finalize
    payment.exported_invoice = True
    payment.save()

    return True

def render_payment(payment):
    # get busy
    payment_details = payment.user.payment_details

    # tax calculations
    tax_percent = float(payment.percent_vat)
    amount_due = float(payment.amount_due)
    amount_vat = round((amount_due / (100.0 + tax_percent)) * tax_percent)
    amount_due_net = amount_due - amount_vat

    # render template
    t = get_template('invoice/invoice.html')
    c = Context({
        "payment_details": payment_details,
        "payment": payment,
        "lines": json.loads(payment.details) if payment.details else {},
        "percent_vat": payment.percent_vat,
        "payment_info": {
            "amount_vat": amount_vat,
            "amount_due_net": amount_due_net
        }
    })
    return t.render(c)

#
# Final url for the payment
#
def url_for_payment(payment):
    return  "https://docs.videopath.com/public/invoices/" + str(payment.pk)


#
# Calculate the filename for the invoice
#
def _key_for_payment(payment):
    dev_prefix = "dev-" if not settings.PRODUCTION else ""
    return settings.AWS_DOCS_INVOICE_PREFIX + dev_prefix + payment.date.strftime('%Y-%m-%d') + "-" + str(payment.id)
