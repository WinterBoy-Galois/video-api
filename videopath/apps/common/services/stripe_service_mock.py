
# test users
STRIPE_CUSTOMER_WITH_CARD = "cus_4kcWGla0DENebP"
STRIPE_CUSTOMER_WITHOUT_CARD = "cus_4kcYOdXJiobmhD"

#
# Get the card for a certain user
#
def get_card_for_user(user):
    return {
    	"last4": "1234",
    	"exp_year": "2015",
    	"exp_month": "8"
    }

#
# Set a card from a token
#
def set_card_for_user(user, token):
    return True


#
# charge user a certain amount
#
def charge_user(user, amount, currency):
	try:
		return "some id" if  user.stripe_id.key == STRIPE_CUSTOMER_WITH_CARD else False
	except:
		return False

#
# Test access to stripe
#
def check_access():
    return True