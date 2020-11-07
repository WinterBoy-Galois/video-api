#
# Removes all example users from the DB
#
from videopath.apps.common.actions import ActionException

from videopath.apps.users.models import User

EMAIL_SUFFIX = 'example.com'

def run():
	
	example_users = User.objects.filter(email__endswith=EMAIL_SUFFIX)
	for u in example_users:
		u.delete()	

