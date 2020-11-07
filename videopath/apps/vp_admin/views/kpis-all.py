

from django.template.response import SimpleTemplateResponse
from .decorators import group_membership_required

from videopath.apps.vp_admin.views import helpers

from videopath.apps.vp_admin.views import viewsets

def build_overall_section():
	result = helpers.header("Overall")
	result += helpers.table([
			['Users', viewsets.all_users().count()],
			['Projects (incl. deleted)', viewsets.all_videos().count()],
			['Published Projects', viewsets.published_videos().count()],
			['Shared Projects', viewsets.shared_videos().count()],
			['Upgraded', viewsets.upgraded_users().count()]
			]);
	return result

def build_graphs():

	result = helpers.header("Signups")
	result += helpers.dategraph(
		viewsets.all_users(), 
		"date_joined", 
		accumulate=False)

	#result += helpers.header("Active Users")
	#result += helpers.dategraph(
	#	viewsets.all_users(), 
	#	"date_joined", 
	#	accumulate=False)

	result += helpers.header("Projects (incl. deleted)")
	result += helpers.dategraph(
		viewsets.all_videos(), 
		"created", 
		accumulate=False)

	result += helpers.header("Published Projects")
	result += helpers.dategraph(
		viewsets.published_videos(),
		"created", 
		accumulate=False)

	result += helpers.header("Shared Projects")
	result += helpers.dategraph(
		viewsets.shared_videos(), 
		"created", 
		accumulate=False)

	result += helpers.header("Plays")
	result += helpers.dategraph(
		viewsets.all_daily_stats(), 
		"date", 
		aggregate_field='plays_all')

	result += helpers.header("Player loads")
	result += helpers.dategraph(
		viewsets.all_daily_stats(), 
		"date", 
		aggregate_field='sessions')

	result += helpers.header("Upgraded")
	result += helpers.dategraph(
		viewsets.upgraded_users(), 
		"date_joined", 
		accumulate=False)
	return result

# build the view
@group_membership_required('insights')
def view(request):

	result = build_overall_section()
	result += build_graphs()

	return SimpleTemplateResponse("insights/base.html", {
	    "title": "KPIs",
	    "insight_content": result
	    })


