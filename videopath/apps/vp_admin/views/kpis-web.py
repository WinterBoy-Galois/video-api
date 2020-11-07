from datetime import timedelta, date
import itertools

from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse
from videopath.apps.users.models import User
from django.core.cache import cache
from .decorators import group_membership_required

from videopath.apps.vp_admin.views import helpers
from videopath.apps.videos.models import Video


from videopath.apps.analytics.services.ga_import_service import _get_service

def website_traffic(service, start, end):

	args = {
        'ids': 'ga:80030959',
        'metrics': 'ga:sessions',
        'start_date': start + 'daysAgo',
        'end_date': end + 'daysAgo',
        'dimensions': 'ga:week,ga:year'
    }

	result = service.data().ga().get(**args).execute()
	result = sorted(result['rows'], key=lambda x: -1 * x[0] + x[1]*100)
	result = map(lambda x: ['week '  + str(x[0]) + ' ' + str(x[1]), int(x[2])], result)
	return helpers.chart([['Week', 'Visitors']] + result, 'line')

def website_traffic_sources(service, start, end):
	args = {
        'ids': 'ga:80030959',
        'metrics': 'ga:sessions',
        'start_date': start + 'daysAgo',
        'end_date': end + 'daysAgo',
        'dimensions': 'ga:channelGrouping'
    }

	result = service.data().ga().get(**args).execute()['rows']
	result = map(lambda x: [x[0], int(x[1])], result)
	result = sorted(result, key=lambda x:x[1])

	return helpers.chart([['Channel', 'Visitors']] + result, 'column')

def blog_traffic(service, start, end):
	args = {
        'ids': 'ga:80030959',
        'metrics': 'ga:sessions',
        'start_date': start + 'daysAgo',
        'end_date': end + 'daysAgo',
        'dimensions': 'ga:week,ga:year',
        'filters': 'ga:pagePath=~/blog*'
    }

	result = service.data().ga().get(**args).execute()
	result = sorted(result['rows'], key=lambda x: -1 * x[0] + x[1]*100)
	result = map(lambda x: ['week ' + str(x[0]) + ' ' + str(x[1]), int(x[2])], result)

	return helpers.chart([['Week', 'Visitors']] + result, 'line')

def blog_traffic_sources(service, start, end):
	args = {
        'ids': 'ga:80030959',
        'metrics': 'ga:sessions',
        'start_date': start + 'daysAgo',
        'end_date': end + 'daysAgo',
        'dimensions': 'ga:channelGrouping',
       	'filters': 'ga:pagePath=~/blog*'
    }

	result = service.data().ga().get(**args).execute()['rows']
	result = map(lambda x: [x[0], int(x[1])], result)
	result = sorted(result, key=lambda x:x[1])


	return helpers.chart([['Channel', 'Visitors']] + result, 'column')

def player_loaded(service, start, end):
	args = {
        'ids': 'ga:83927052',
        'metrics': 'ga:sessions',
        'start_date': start + 'daysAgo',
        'end_date': end + 'daysAgo',
        'dimensions': 'ga:week,ga:year',
    }

	result = service.data().ga().get(**args).execute()
	result = sorted(result['rows'], key=lambda x: -1 * x[0] + x[1]*100)
	result = map(lambda x: ['week ' + str(x[0]) + ' ' + str(x[1]), int(x[2])], result)
	return helpers.chart([['Week', 'Visitors']] + result, 'line')

def player_played(service, start, end):
	args = {
        'ids': 'ga:83927052',
        'metrics': 'ga:uniqueEvents',
        'start_date': start + 'daysAgo',
        'end_date': end + 'daysAgo',
        'filters': 'ga:eventAction==play',
        'dimensions': 'ga:week,ga:year',
    }

	result = service.data().ga().get(**args).execute()
	result = sorted(result['rows'], key=lambda x: -1 * x[0] + x[1]*100)
	result = map(lambda x: ['week ' + str(x[0]) + ' ' + str(x[1]), int(x[2])], result)
	return helpers.chart([['Week', 'Visitors']] + result, 'line')

# build the view
@group_membership_required('insights')
def view(request):
	# default to year weeks
	get = request.GET

	start = get.get('start', '-100')
	end = get.get('end', '0')

	# # redirect if args are missing
	if not "start" in get or not "end" in get:
		return HttpResponseRedirect("/admin/insights/kpis-web/?start="+start+"&end="+end)

	# sanitize start and end
	start = str(int(start) * -1)
	end = str(int(end) * -1)

	service = _get_service()

	result = ""

	result += helpers.header("Website traffic")
	result += website_traffic(service, start, end)

	result += helpers.header("Website traffic sources")
	result += website_traffic_sources(service, start, end)

	result += helpers.header("Blog traffic (all urls starting with /blog)")
	result += blog_traffic(service, start, end)

	result += helpers.header("Blog traffic sources")
	result += blog_traffic_sources(service, start, end)

	result += helpers.header("Player loaded")
	result += player_loaded(service, start, end)

	result += helpers.header("Player plays")
	result += player_played(service, start, end)

	return SimpleTemplateResponse("insights/base.html", {
	    "title": "KPIs Web",
	    "insight_content": result
	    })


