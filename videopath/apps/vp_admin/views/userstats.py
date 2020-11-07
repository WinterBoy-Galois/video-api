from datetime import timedelta, date
from django.db.models import Sum

from django.template.response import SimpleTemplateResponse

from .decorators import group_membership_required

from videopath.apps.vp_admin.views import helpers
from videopath.apps.vp_admin.views import viewsets

@group_membership_required('insights')
def view(request):
    result = ""

    #
    # Most views
    #
    result += helpers.header("Users with the most views on their projects")

    count = viewsets.all_videos().values('team__owner__username').annotate(score=Sum("total_plays")).order_by('-score')
    max_rows = 25
    result_array = []
    for entry in count:
        result_array.append([
                helpers.userlink(entry["team__owner__username"]),
                str(entry["score"])
            ])
        max_rows -= 1
        if max_rows == 10: break
    result += helpers.table(result_array, ["username", "plays"])

    #
    # Seen in last 30 days
    #
    enddate = date.today() - timedelta(days=30)
    daily_data = viewsets.user_activity_daily().filter(day__gt=enddate)

    userlist = {}
    for data in daily_data:
        if data.day == data.user.date_joined.date():
            continue
        username = data.user.username
        if not username in userlist:
            userlist[username] = [username, 0]
        userlist[username][1]+=1

    userlist = userlist.values()
    userlist.sort(key=lambda x: -x[1])
    userlist = map(lambda x: [helpers.userlink(x[0]), str(x[1]) + " days"], userlist)

    result += helpers.header("Users seen in last 30 days")
    result += "Users seen on the same day as they signed up are stripped out<br /> <br />"
    result += helpers.table(userlist)


    return SimpleTemplateResponse("insights/base.html", {
        "title": "User statistics",
        "insight_content": result
        })
