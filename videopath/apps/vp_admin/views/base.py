from datetime import timedelta, datetime

from videopath.apps.users.models import User
from .decorators import group_membership_required
from django.template.response import SimpleTemplateResponse

from videopath.apps.users.models import UserActivity
from videopath.apps.videos.models import Video
from videopath.apps.vp_admin.views import helpers


@group_membership_required('insights')
def view(request):

    result = helpers.header("General Stats")

    # no of accounts
    all_users = User.objects.all().order_by("username")
    result += "Number of user accounts: " + str(all_users.count()) + "\n"

    # general stats videos
    all_videos = Video.objects.all()
    all_demos = Video.objects.filter(
        draft__source__service_identifier="2rtGFAnyf-s").count()
    all_videos_published = Video.objects.filter(published=Video.PUBLIC)
    all_demos_published = Video.objects.filter(
        draft__source__service_identifier="2rtGFAnyf-s", published=Video.PUBLIC).count()
    result += "Number of video projects: " + \
        str(all_videos.count()) + " (" + str(all_demos) + " demos) \n"
    result += "Number of published video projects: " + \
        str(all_videos_published.count()) + \
        " (" + str(all_demos_published) + " demos) \n"


    result += helpers.header("Activity")

    # active in last 7 days
    startdate = datetime.now()
    enddate = startdate - timedelta(days=7)
    last_activities = UserActivity.objects.filter(
        last_seen__range=[enddate, startdate]).order_by('-last_seen')
    result += "Active in last 7 days: " + str(last_activities.count()) + "\n"

    # signups in last 7 days
    last_activities = User.objects.filter(
        date_joined__range=[enddate, startdate]).order_by('-last_seen')
    result += "Signups in last 7 days: " + str(last_activities.count()) + "\n"

    startdate = datetime.now()
    enddate = startdate - timedelta(days=30)
    last_activities = UserActivity.objects.filter(
        last_seen__range=[enddate, startdate]).order_by('-last_seen')
    result += "Active in last 30 days: " + str(last_activities.count()) + "\n"

    # signups in last 7 days
    last_activities = User.objects.filter(
        date_joined__range=[enddate, startdate]).order_by('-last_seen')
    result += "Signups in last 30 days: " + str(last_activities.count()) + "\n"

    return SimpleTemplateResponse("insights/base.html", {
        "title": "Insights Home",
        "insight_content": result
        })
