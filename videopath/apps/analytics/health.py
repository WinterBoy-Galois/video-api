from datetime import date, timedelta

from django.conf import settings

from videopath.apps.analytics.services import ga_import_service
from videopath.apps.analytics.models import DailyAnalyticsData

def check_access_to_google_analytics():
	return ga_import_service.check_access()

def check_imports():
	if settings.STAGING:
		return True
	twodaysago = date.today() - timedelta(2)
	count = DailyAnalyticsData.objects.filter(date=twodaysago).count()
	if count == 0:
		return "There appear to be no recent google analytics imports!"
	else:
		return True

