from datetime import timedelta, datetime, date

from django.template.response import SimpleTemplateResponse
from django.db.models import Sum
from .decorators import group_membership_required

from videopath.apps.videos.models import Video
from videopath.apps.analytics.models import DailyAnalyticsData, VideoStatistics
from videopath.apps.vp_admin.views import helpers

import math

@group_membership_required('insights')
def listview(request):

    # video plays
    result = helpers.header("Plays of videos by user in the last 7 days")
    last_day = date.today()
    first_day = last_day - timedelta(days=7)
    count = DailyAnalyticsData.objects.filter(
        date__gte=first_day,
        date__lt=last_day)\
        .values('video__team__owner__username')\
        .annotate(score=Sum("plays_all"))\
        .order_by('-score')

    rows = 0
    result_array = []
    for entry in count:
        result_array.append([
                entry["video__team__owner__username"],
                str(entry["score"])
            ])
        rows += 1
        if rows >= 10: break
    result += helpers.table(result_array, ["username", "plays"])

    #
    # Popular videos
    #
    result += helpers.header("Most popular video the last 7 days")
    last_day = date.today()
    first_day = last_day - timedelta(days=7)
    count = DailyAnalyticsData.objects.filter(
        date__gte=first_day,
        date__lt=last_day)\
        .values('video_id')\
        .annotate(score=Sum("plays_all"))\
        .order_by('-score')


    result_array = []
    max_rows = 25
    for entry in count:
        video = Video.objects.get(pk=entry["video_id"])
        link = helpers.videolink(video)
        if link:
            link.append(entry['score'])
            result_array.append(link)
        max_rows -= 1
        if max_rows == 0: break


    result += helpers.table(result_array, ["Title", "User", "Modified", "Plays all", "Plays last 7"])



    #
    # published vids
    #
    startdate = datetime.now()
    enddate = startdate - timedelta(days=30)
    result += helpers.header("Recently published videos")
    videos = Video.objects.filter(current_revision__modified__range=[enddate, startdate]).order_by('-current_revision__modified')
    result += helpers.videolist(videos) 


    return SimpleTemplateResponse("insights/base.html", {
        "title": "Videos",
        "insight_content": result
        })


def formatSeconds(s):
    if not s: s = 0 
    s = math.floor(s)
    return str(timedelta(seconds=s))


@group_membership_required('insights')
def videoview(request, key):
    video = Video.objects.get(key=key)

    result = helpers.header("General Info")
    result += "User: " + helpers.userlink(video.team.owner)

    result += helpers.header("Overall stats")
    try:
        data = video.total_analytics.latest("plays_all")

        percent_interacting = int(min(100, (float(data.overlays_opened_unique / float(data.plays_all)) * 100)))
        clicks_per_user = (float(data.overlays_opened_all) / float(data.plays_all))

        result += "Plays: " + str(data.plays_all) + "\n"
        result += "Plays unique: " + str(data.plays_unique) + "\n"
        result += "Average Session Duration: " + str(data.avg_session_time) + "\n"
        result += "Clicks on markers: " + str(data.overlays_opened_all) + "\n"
        result += "Clicks on markers unique: " + str(data.overlays_opened_unique) + "\n"
        result += "Viewers interacting: " + str(percent_interacting) + "%\n"
        result += "Average clicks per user: " + str(clicks_per_user) + "\n"

    except:
        result += "No stats available at this time"

    result += helpers.header("Engagement stats")
    try:

        # overall stats
        querySet = VideoStatistics.objects.filter(videoKey=key, sessionTotal__lte = 1800)

        stats =  querySet.aggregate(playingTotal = Sum('playingTotal'), overlayOpenTotal = Sum('overlayOpenTotal'), sessionTotal = Sum('sessionTotal'))
        num_sessions = str(querySet.count())
        result += "Recorded Sessions: " + num_sessions + "\n"
        result += "Overall session time: " + formatSeconds(stats['sessionTotal']) + " - avg. "  + formatSeconds( stats['sessionTotal'] / float(num_sessions))   + "\n"
        result += "Overall play time: " + formatSeconds(stats['playingTotal']) + " - avg. " + formatSeconds( stats['playingTotal'] / float(num_sessions)) + "\n"
        result += "Overall overlay time: " + formatSeconds(stats['overlayOpenTotal']) +  " - avg. " + formatSeconds( stats['overlayOpenTotal'] / float(num_sessions)) + "\n"
        result += "<strong>Time spent longer on video: " + str(math.ceil(stats['overlayOpenTotal'] / stats['sessionTotal'] * 100)) + '% </strong>'

        # sessions with overlay opens
        result += '<br /><br /><strong>Session with overlay opens</strong><br />'
        querySet = VideoStatistics.objects.filter(videoKey=key, sessionTotal__lte = 1800, overlayOpenTotal__gt = 10 )

        stats =  querySet.aggregate(playingTotal = Sum('playingTotal'), overlayOpenTotal = Sum('overlayOpenTotal'), sessionTotal = Sum('sessionTotal'))
        num_sessions = str(querySet.count())
        result += "Recorded Sessions: " + num_sessions + "\n"
        result += "Overall session time: " + formatSeconds(stats['sessionTotal']) + " - avg. "  + formatSeconds( stats['sessionTotal'] / float(num_sessions))   + "\n"
        result += "Overall play time: " + formatSeconds(stats['playingTotal']) + " - avg. " + formatSeconds( stats['playingTotal'] / float(num_sessions)) + "\n"
        result += "Overall overlay time: " + formatSeconds(stats['overlayOpenTotal']) +  " - avg. " + formatSeconds( stats['overlayOpenTotal'] / float(num_sessions)) + "\n"
        result += "<strong>Time spent longer on video: " + str(math.ceil(stats['overlayOpenTotal'] / stats['sessionTotal'] * 100)) + '% </strong>'
    except:
        result += "No data available at this time"

    result += helpers.header("Video")
    result += '<iframe width="700px" height="525px" frameborder="0" src="https://player.videopath.com/' + video.key + '" allowfullscreen="" onmousewheel="event.preventDefault();"></iframe>'

    return SimpleTemplateResponse("insights/base.html", {
        "title": "Video '" + video.get_current_revision_or_draft().title + "'",
        "insight_content": result
        })
