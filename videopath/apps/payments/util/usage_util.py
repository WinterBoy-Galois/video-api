from datetime import date
from dateutil.relativedelta import relativedelta

from django.db.models import Sum

from videopath.apps.analytics.models import DailyAnalyticsData

#
# Calculate usage of a user
#
def plan_usage(user, relative_month=0):
    td = date.today()
    td -= relativedelta(months=relative_month)
    first_day = date(td.year, td.month, 1)
    last_day = first_day + relativedelta(months=1)
    count = DailyAnalyticsData.objects.filter(
        video__team__owner=user,
        date__gte=first_day,
        date__lt=last_day
    ).aggregate(Sum("plays_all"))
    result = count["plays_all__sum"]
    return result if result else 0


#
# Usage of current month
#
def plan_usage_current(user):
    return plan_usage(user)


#
# Usage during last month
#
def plan_usage_last(user):
    return plan_usage(user, 1)
