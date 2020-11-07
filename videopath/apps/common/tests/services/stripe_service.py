from videopath.apps.common.test_utils import BaseTestCase

from videopath.apps.common.services import service_provider
from videopath.apps.payments.models import StripeID

STRIPE_CUSTOMER_WITH_CARD = "cus_4kcWGla0DENebP"
STRIPE_CUSTOMER_WITHOUT_CARD = "cus_4kcYOdXJiobmhD"

# Uses the standard django frame testing client
class TestClass(BaseTestCase):

    def setup(self):
    	self.create_user()
        self.service = service_provider.get_service("stripe")
        self.assertIsNotNone(self.service)


    def test_cards(self):
        StripeID.objects.create(user=self.user, key=STRIPE_CUSTOMER_WITH_CARD)
        card = self.service.get_card_for_user(self.user)
        self.assertNotEqual(card, None)

    def test_charge_success(self):
        StripeID.objects.create(user=self.user, key=STRIPE_CUSTOMER_WITH_CARD)
        result = self.service.charge_user(self.user, 20000, "usd")
        self.assertNotEqual(result, False)

    def test_charge_fail(self):
        StripeID.objects.create(
            user=self.user, key=STRIPE_CUSTOMER_WITHOUT_CARD)
        result = self.service.charge_user(self.user, 20000, "eur")
        self.assertFalse(result)
