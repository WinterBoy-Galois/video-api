from datetime import datetime, timedelta, date

from django.core.cache import cache

from rest_framework import exceptions

from videopath.apps.users.models import APIToken, AuthenticationToken, UserActivity, UserActivityDay
from videopath.apps.common.services import service_provider

def authenticate_token(key):
	
	# try to load user and token from key	
	user, token = _load_user_and_token(key)

	try:
		# last seen
		_track_activity(user)
		# last seen per day
		_track_activity_daily(user)
	except:
		pass

	return user, token

#
# Try to validate access token
#
def _load_user_and_token(key):
	# try to find user in cache
	user = cache.get(key + "-user")
	token = cache.get(key + "-token")

	# try to find token
	if not user or not token:
	    try:
	        token = AuthenticationToken.objects.get(key=key)
	        user = token.user
	        cache.set(key + "-user", user, 60 * 5)  # save for 5 minutes
	        cache.set(key + "-token", token, 60 * 5)  # save for 5 minutes
	    except AuthenticationToken.DoesNotExist:
	    	try: 
	    		token = APIToken.objects.get(key=key)
	        	user = token.user
	       	 	cache.set(key + "-user", user, 60 * 5)  # save for 5 minutes
	        	cache.set(key + "-token", token, 60 * 5)  # save for 5 minutes
	        except APIToken.DoesNotExist:
	        	raise exceptions.AuthenticationFailed('Invalid token')

	#
	if not user.is_active:
	    raise exceptions.AuthenticationFailed('User inactive or deleted')

	# update last used timestamp if it's older than 10 minutes
	thresh = datetime.now() - timedelta(minutes=10)
	if token:
	    if token.last_used < thresh:
	        token.last_used = datetime.now()
	        token.save()

	return user, token


#
# keep a log of the last activity time
#
def _track_activity(user):
	thresh = datetime.now() - timedelta(minutes=10)
	cachekey = user.username + "-activity"
	activity = cache.get(cachekey)
	if not activity:
	    try:
	        activity = user.activity
	    except UserActivity.DoesNotExist:
	        activity, created = UserActivity.objects.get_or_create(user=user)
	        activity.last_seen=datetime.now()
	        activity.save()
	    cache.set(cachekey, activity)

	if activity and (not activity.last_seen or activity.last_seen < thresh):
	    activity.last_seen = datetime.now()
	    activity.save()
	    cache.set(cachekey, activity)

#
# Keep a log of when the users were here
#
def _track_activity_daily(user):
	today = date.today()
        cachekey = user.username + "-day-" + str(today)
        activity = cache.get(cachekey)
        if not activity:
            activity, created = UserActivityDay.objects.get_or_create(user=user, day=today)
            cache.set(cachekey, activity)
            if created:
				slack = service_provider.get_service("slack")
				visitors_today = UserActivityDay.objects.filter(day=today).count()
				visited_days = UserActivityDay.objects.filter(user=user).count()
				slack.notify("User " + user.email + " just seen for the first time today. This is our " + str(visitors_today) + ". visitor today. This user has been seen on " + str(visited_days) + " days since he has signed up.")
