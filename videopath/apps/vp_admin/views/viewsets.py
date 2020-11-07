
from videopath.apps.users.models import User
from videopath.apps.videos.models import Video
from videopath.apps.users.models import UserActivityDay

from videopath.apps.analytics.models import TotalAnalyticsData



company_accounts = [
    "david",
    "product_demo", #company
    "marketing", # company
    "huesforalice", # dave
    "anna",
    "tim t", #tim 2
    "tim", # tim 1
    "trival", # thomas
    "nimaa", 
    "lcdenison", # louisa 1
    "dontdelete", # louisa 2
    "yana",
    "jolly",
    "junayd",
    "vp_test_basic",
    "vp_test_pro",
    "vp_test_enterprise",
    "desiree@videopath.com",
    "anila@videopath.com",
    "adillon_88@hotmail.com"
]

non_paid_plans = [
	"free-free",
	"individual-staff",
	"individual-agency-evaluation"
]


#
# users
#
def all_users():
	viewset = User.objects.exclude(username__in=company_accounts)
	return viewset

def upgraded_users():
	viewset = all_users()
	viewset = viewset.exclude(subscription__isnull=True)
	viewset = viewset.exclude(subscription__plan__in=non_paid_plans)
	return viewset

def active_users():
	pass

def user_activity_daily():
	viewset = UserActivityDay.objects.exclude(user__username__in=company_accounts)
	return viewset

#
# videos
#
def all_videos():
	viewset = Video.objects.exclude(team__owner__username__in=company_accounts)
	return viewset

def published_videos():
	viewset = all_videos().filter(published=True)
	return viewset

def shared_videos():
	viewset = all_videos().filter(total_plays__gte=50)
	return viewset

#
# VIdeo stats
#
def all_total_analytics():
	viewset = TotalAnalyticsData.objects.exclude(video__team__owner__username__in=company_accounts)
	return viewset
	

#
# daily stats
#
def all_daily_stats():
	from videopath.apps.analytics.models import DailyAnalyticsData
	viewset = DailyAnalyticsData.objects.exclude(video__team__owner__username__in=company_accounts)
	return viewset



