from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.payments.models import Payment, PaymentDetails
from videopath.apps.payments.util import payment_util

class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()
        self.payment = Payment.objects.create(user=self.user, amount_due=200)

    def test_creation(self):

    	# no payment should be created if nothing is owed
        PaymentDetails.objects.create(user=self.user, country="Germany")
    	payment = payment_util.create_payment(self.user, [], "eur")
    	self.assertEquals(payment,None)

    	# expect payment to be created properly
    	payment = payment_util.create_payment(self.user, [{
    		"text":"one line",
    		"amount": 200
    		}], "eur")
    	self.assertEquals(payment.amount_due,200)
        self.assertEquals(payment.percent_vat,19)

    def test_processing(self):
        PaymentDetails.objects.create(user=self.user, country="United Kingdom")
    	payment_util.process_payments()

    def test_creation_with_eu_vat(self):
        # expect payment to be created properly
        PaymentDetails.objects.create(user=self.user, country="United Kingdom")
        payment = payment_util.create_payment(self.user, [{
            "text":"one line",
            "amount": 200
            }], "eur")
        self.assertEquals(payment.amount_due,200)
        self.assertEquals(payment.percent_vat, 20)

    def test_creation_with_us_vat(self):
        # expect payment to be created properly
        PaymentDetails.objects.create(user=self.user, country="United States")
        payment = payment_util.create_payment(self.user, [{
            "text":"one line",
            "amount": 200
            }], "eur")
        self.assertEquals(payment.amount_due,200)
        self.assertEquals(payment.percent_vat, 0)
        

