
from datetime import datetime, timedelta
from ..actions import move_user_to_pipedrive
from ..models import User

def run():
	cutoff = datetime.today() -  timedelta(days=1)
	users = User.objects.filter(sales_info=None, date_joined__gte=cutoff)

	for u in users:
		move_user_to_pipedrive.run(u)
