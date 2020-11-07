import datetime
import stripe

from django.http import HttpResponse
from .decorators import group_membership_required

from videopath.apps.payments.models import Payment, PaymentDetails


def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(
        int(timestamp)
        ).strftime('%d.%m.%Y')

def convert_amount(amount):
    return "{:2.2f}".format(amount/100.0)

@group_membership_required('insights')
def view(request):

    table = []

    table.append([
        "Type",
        "Date",
        "Gross",
        "Stripe Fees",
        "w/o Fees",
        "Currency",
        "Vat %",
        "Invoice No",
        "Adress"
        ])
    table.append(["=="])

    transfers = stripe.Transfer.all(limit=100)
    for t in transfers.data:
        table.append([
            "Transaction",
            convert_timestamp(t.date),
            convert_amount(t.summary.charge_gross),
            convert_amount(t.summary.charge_fees),
            convert_amount(t.summary.net),
            t.currency
            ])

        for ta in t.transactions.data:
            # load payment
            payment = None
            address = None

            try:
                payment = Payment.objects.get(transaction_id=ta.id)
                pd = payment.user.payment_details
                address = pd.name + ", " + pd.street + ", " + pd.post_code + " " + pd.city + ", " + pd.country
            except Payment.DoesNotExist:
                pass
            except PaymentDetails.DoesNotExist:
                pass


            table.append([
                "Transfer",
                convert_timestamp(ta.created),
                convert_amount(ta.amount),
                convert_amount(ta.fee),
                convert_amount(ta.net),
                ta.currency,
                str(payment.percent_vat) if payment else "--",
                "a01-"+str(payment.number) if payment else "--",
                address if address else "--",
                ])
        table.append(["=="])

    result = ""

    # build csv
    for row in table:   
        for col in row:
            result += '"' + col + '",'
        result += "\n"

    response = HttpResponse(result, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    return response
