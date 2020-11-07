from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.payments.models import Payment, PaymentDetails
from videopath.apps.payments.util import payment_export_util

class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()
        self.payment = Payment.objects.create(user=self.user)
        self.payment_details = PaymentDetails.objects.create(user=self.user)

    def test_export(self):
        payment_export_util.export_payment(self.payment)

