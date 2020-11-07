import humanize
from urlparse import urlparse

from videopath.apps.users.models import User
from .decorators import group_membership_required
from django.template.response import SimpleTemplateResponse


from videopath.apps.videos.models import Video
from videopath.apps.vp_admin.views import helpers
from videopath.apps.vp_admin.views import viewsets

from videopath.apps.payments.actions import start_trial

@group_membership_required('insights')
def listview(request):
    result = ""
    users = []
    for u in User.objects.all():
        videos = Video.objects.filter_for_user.filter(archived=False).count()

        # published
        videos_published = u.videos.filter(published=Video.PUBLIC, archived=False).count()
        demo_videos = Video.objects.filter(
            video__team__owner=u, service_identifier="2rtGFAnyf-s").count()

        if videos == 0:
            color = "red"
        elif videos > 0 and videos_published == 0 or demo_videos == videos:
            color = "darkorange"
        else:
            color = "green"

        user = [
            "<span style = 'color:" + color + "'>" + helpers.userlink(u) + "</span>",
            "<b>" + str(videos) + "</b> videos",
            "<b>" + str(videos_published) + "</b> published",
            "<b>" + str(demo_videos) + "</b> demos"
        ]
        users.append(user)
    result += helpers.table(users)

    return SimpleTemplateResponse("insights/base.html", {
        "title": "All Users",
        "insight_content": result
        })


def referral_link(url):
        if url:
            parsed_uri = urlparse( url )
            return '<a href="' + url + '">' + parsed_uri.netloc +'</a><br />';
        return ''

@group_membership_required('insights')
def listview_sales(request):

    result = ""
    users = []

    for u in User.objects.extra(select={
            'campaign_name': 'SELECT name FROM users_usercampaigndata WHERE users_usercampaigndata.user_id = auth_user.id',
            'country': 'SELECT country FROM users_usercampaigndata WHERE users_usercampaigndata.user_id = auth_user.id',
            'referrer': 'SELECT referrer FROM users_usercampaigndata WHERE users_usercampaigndata.user_id = auth_user.id',
            'num_videos': 'SELECT COUNT(*) FROM videos_video JOIN users_team  ON (videos_video.team_id = users_team.id) WHERE users_team.owner_id = auth_user.id AND videos_video.archived != True',
            'num_videos_published': 'SELECT COUNT(*) FROM videos_video JOIN users_team  ON (videos_video.team_id = users_team.id) WHERE users_team.owner_id = auth_user.id AND videos_video.archived != True AND videos_video.published = 1',
        }).order_by('-date_joined'):
        user = [
            "<span>" + helpers.userlink(u) + "</span>",
            u.email,
            "" + str(u.country if u.country else '') + "",
            "" + str(u.campaign_name if u.campaign_name else '') + "",
            referral_link(u.referrer),
            "<b>" + str(u.num_videos) + "</b> v",
            "<b>" + str(u.num_videos_published) + "</b> p",
            "<b>"+str(u.date_joined.date())+ "</b>",
        ]
        users.append(user)

    result += helpers.table(users)

    return SimpleTemplateResponse("insights/base.html", {
        "title": "All Users (Sales List)",
        "insight_content": result
        })

@group_membership_required('insights')
def userview(request, username):


    

    # load user
    user = User.objects.get(username=username)

    # start trial if requested
    if request.GET.get('trial', False):
        start_trial.run(user)

    result = helpers.header("Info")
    result += "<a href='mailto:"+user.email+"'>" + user.email+ "</a> <br />"
    result += "Signed up " + humanize.naturaltime(user.date_joined) + "<br />"

    # last seen info
    try:
        result += "Last seen " + humanize.naturaltime(user.activity.last_seen) + "<br />"
    except:
        pass

    try:
        result += "Currently subscribed to " + user.subscription.plan + "<br />"
    except:
        pass

    result += "<br /><a href ='{0}?trial=true'>Start Trial</a>".format(request.path)

    # billing info
    result += helpers.header("Billing Adress")
    try:
        result += user.payment_details.name + "<br />"
        result += user.payment_details.street + "<br />"
        result += user.payment_details.city + "<br />"
        result += user.payment_details.post_code + "<br />"
        result += user.payment_details.country + "<br />"
    except:
        pass

    # camaign info
    result += helpers.header("Campaign Info")
    try:
        result += "Country: " + user.campaign_data.country + "<br />"
        result += "Referrer: " + referral_link(user.campaign_data.referrer) + "<br />"
        result += "<br />"
        result += "Name: " + user.campaign_data.name + "<br />"
        result += "Source: " + user.campaign_data.source + "<br />"
        result += "Medium: " + user.campaign_data.medium + "<br />"
        result += "Content: " + user.campaign_data.content + "<br />"
        result += "Term: " + user.campaign_data.term + "<br />"
    except:
        pass

    result += helpers.header("Video plays")
    result += helpers.dategraph(
        viewsets.all_daily_stats().filter(video__team__owner=user), 
        "date", 
        aggregate_field='plays_all')

    result += helpers.header("Days seen per week")
    result += helpers.dategraph(
        user.user_activity_day.all(), 
        "day")


    # published videos 
    result += helpers.header("Published Videos")
    videos = Video.objects.filter(team__owner=user, archived=False, published=Video.PUBLIC).order_by('-current_revision__modified')
    result += helpers.videolist(videos)

    # unpublished videos
    result += helpers.header("Unpublished Videos")
    videos = Video.objects.filter(team__owner=user,archived=False, published=Video.PRIVATE).order_by('-current_revision__modified')
    result += helpers.videolist(videos)

    # deleted projects videos
    result += helpers.header("Deleted Videos")
    videos = Video.objects.filter(team__owner=user, archived=True).order_by('-current_revision__modified')
    result += helpers.videolist(videos)


    return SimpleTemplateResponse("insights/base.html", {
        "title": "User '" + username + "'",
        "insight_content": result
        })
