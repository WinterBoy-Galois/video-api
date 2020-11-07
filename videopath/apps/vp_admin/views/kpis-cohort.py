from datetime import timedelta, date
import itertools

from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse
from videopath.apps.users.models import User
from django.core.cache import cache
from .decorators import group_membership_required

from videopath.apps.vp_admin.views import helpers
from videopath.apps.videos.models import Video


cohorte_selectors = {
    "week": "%G %V",
    "month": "%Y %m",
    "year": "%Y %m"
}

steps = ["has_videos", "has_published_videos", "has_views", "has_upgraded"]


# build a dict of users containing all the relevant info
# for the kpi funnel steps and rentainment
def build_user_info(start_date, end_date):

    retention_step = 30

    # cache results
    cache_key = str(start_date) + str(end_date)
    result = cache.get(cache_key)
    if result:
        return result

    users = User.objects.filter(date_joined__lte=end_date, date_joined__gte=start_date).order_by('date_joined')
    result = []

    def map_user(user):
        has_upgraded = False
        try:
            user.subscription
            if not "free" in user.subscription.plan:
                has_upgraded = True
        except:
            pass

        user_videos = Video.objects.filter(team__owner=user)

        activation = {
            "signed_up": True,
            "has_videos": user_videos.count() > 0,
            "has_published_videos": user_videos.filter(published=Video.PUBLIC).count() > 0,
            "has_views": user_videos.filter(total_plays__gte=10).count() > 0,
            "has_upgraded": has_upgraded
        }

        retention = {}

        date = user.date_joined + timedelta(days=1)

        # implement retention
        count = 1
        while date < date.today():
            period_end = date + timedelta(days=retention_step)
            retention[count] = user.user_activity_day.filter(day__gte=date, day__lt=period_end).count() > 0
            date = period_end
            count+=1

        return {
            "date_joined": user.date_joined,
            "activation": activation,
            "retention": retention
        }

    result = map(map_user, users)

    cache.set(cache_key, result , 60 * 5)

    return result

# group users into cohorte sampple sizes
def group_users(users, cohorte_selector):
    groups = itertools.groupby(users, lambda user:user["date_joined"].strftime(cohorte_selector))

    def map_groups(group):
        result = {
            "cohorte": group[0],
            "size":0,
            "activation":{},
            "retention":{}
        }

        for step in steps:
            result["activation"][step]=0

        for i in range(1,12):
            result["retention"][i] = 0

        for user in group[1]:
            result["size"] += 1

            # activation
            for step in steps:
                result["activation"][step] += 1 if user["activation"][step] else 0

            # retention
            for step in user["retention"]:
                if step > 12:
                    break
                result["retention"][step] += 1 if user["retention"][step] else 0

        return result

    result = map(map_groups, groups)

    return result


#  Create the activation view
def build_activation_table(groups):


    data = [['week'] + steps]

    for group in groups:
        idata = [group['cohorte']]
        for step in steps:
            idata.append(group["activation"][step] * 100 / group['size'])
        data.append(idata)

    return helpers.chart(data, 'line')


def build_retention_table(groups):


    data = [['week', '-1 month', '-2 months', '-3 months', '-4 months']]

    for group in groups:
        idata = [group['cohorte']]
        for i in range(1,5):
            idata.append(group["retention"][i] * 100 / group['size'])
        data.append(idata)


    return helpers.chart(data, 'line')



# build the view
@group_membership_required('insights')
def view(request):
    
    # default to year weeks
    get = request.GET

    cohorte_size = get.get('cohorte', 'month')
    start = get.get('start', '-100')
    end = get.get('end', '0')

    # redirect if args are missing
    if not "cohorte" in get or not "start" in get or not "end" in get:
        return HttpResponseRedirect("/admin/insights/kpis-cohort/?cohorte="+cohorte_size+"&start="+start+"&end="+end)

    # convert args
    cohorte_selector = cohorte_selectors[cohorte_size]
    start_date = date.today() + timedelta(days=int(start))
    end_date = date.today() + timedelta(days=int(end)+1)

    # build dict of users   
    users = build_user_info(start_date, end_date)
    
   
    result = ""
 
    # info
    result += helpers.header("Report Details")
    result += "Cohorte Size: " + cohorte_size + "<br />"
    result += "Date Range: " + str(start_date) +" " + str(end_date) + "<br />"
    result += "Total signups in range: " + str(len(users))

    groups = group_users(users, cohorte_selector)


    # activiation section
    result += helpers.header("Activation (percentage of signed up)")
    result += build_activation_table(groups)

    # retention section
    result += helpers.header("Retention (percentage of signed up)")
    result += build_retention_table(groups)

    return SimpleTemplateResponse("insights/base.html", {
        "title": "KPIs",
        "insight_content": result
        })


