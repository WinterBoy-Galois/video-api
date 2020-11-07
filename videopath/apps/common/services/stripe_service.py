import stripe

from django.conf import settings

# this should probably not be used here..
# we should have a way of separating services from the
# db layer, at least this would make sense!
from videopath.apps.payments.models import StripeID

stripe.api_key = settings.STRIPE_API_KEY


# test users
STRIPE_CUSTOMER_WITH_CARD = "cus_4kcWGla0DENebP"
STRIPE_CUSTOMER_WITHOUT_CARD = "cus_4kcYOdXJiobmhD"

#
# manage cards
#
def get_card_for_user(user):

    stripe_customer = _get_stripe_customer_for_user(user)
    if not stripe_customer:
        return None

    cards = stripe_customer.sources.all()
    for card in cards.data:
        return card
    return None

#
# Set a card from a token
#
def set_card_for_user(user, token):

    # get reference to stripe customer
    stripe_customer = _get_stripe_customer_for_user(user, True)

    try:
        new_card = stripe_customer.sources.create(card=token)

        # remove excess cards on stripe
        cards = stripe_customer.sources.all()
        for card in cards.data:
            if new_card.id != card.id:
                card.delete()
        return True, "", new_card
    except stripe.error.CardError:
        error = "There was a problem validating your card. Did you enter the correct Number, Expiration Date and CVC?"
    except Exception:
        error = "We currently can't connect to our payment provider. Please try again later."
    return False, error, None


#
# charge user a certain amount
#
def charge_user(user, amount, currency):
    customer = _get_stripe_customer_for_user(user)
    if not customer:
        return False

    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency.lower(),
            customer=customer,
            description="Videopath Subscription"
        )
        return charge.id
    except:
        return False

    return False


#
# Internal function to map users to actual strip customers
#
def _get_stripe_customer_for_user(user, create_if_missing=False):
    try:
        return stripe.Customer.retrieve(user.stripe_id.key)
    except StripeID.DoesNotExist:
        pass

    # create a new one if missing
    if create_if_missing:
        stripe_customer = stripe.Customer.create(
            email=user.email
        )
        StripeID.objects.create(user=user, key=stripe_customer.id)
        return stripe_customer

    return None


#
# Test access to stripe
#
def check_access():
    try:
        stripe.Account.retrieve()
        return True
    except Exception as e:
        return str(e)
