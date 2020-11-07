#
# Expires unused authentication tokens
#

import datetime

from videopath.apps.users.models import AuthenticationToken

def run(self, *args, **options):
    # delete tokens
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    min_last_used = datetime.date.today() - datetime.timedelta(minutes=60)
    for token in AuthenticationToken.objects.filter(created__lt=yesterday, last_used__lt=min_last_used):
    	token.delete()
