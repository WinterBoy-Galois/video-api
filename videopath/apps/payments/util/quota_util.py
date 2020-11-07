from datetime import date
from dateutil.relativedelta import relativedelta

from django.db.models import Sum
from django.conf import settings
from videopath.apps.users.models import User

from videopath.apps.payments.models import QuotaInformation
from videopath.apps.analytics.models import DailyAnalyticsData
from videopath.apps.common import mailer


#
# Check all quotas and send warning mails if needed
#
def check_quotas():

    info = _get_quota_info()

    for entry in info:

        percent_used = float(
            entry["views"]) / float(entry["plan"]["max_views_month"])
        user = User.objects.get(pk=entry["user_id"])
        quota_info = get_user_quota_info(user)

        if percent_used >= 1:
            _handle_user_exceeded(user)
        elif percent_used > 0.8:
            _handle_user_warning(user)
        else:
            quota_info.quota_exceeded = False
            quota_info.warning_sent = False
            quota_info.save()

#
# Get info about the quota of the user
#
def get_user_quota_info(user):
    info, created = QuotaInformation.objects.get_or_create(user=user)
    return info

#
# Get a list of users and their quota information
#
def _get_quota_info():

    td = date.today()
    first_day = date(td.year, td.month, 1)
    last_day = first_day + relativedelta(months=1)
    qresult = DailyAnalyticsData.objects.filter(
        date__gte=first_day,
        date__lt=last_day)\
        .values('video__team__owner__pk', 'video__team__owner__subscription__plan')\
        .annotate(views=Sum("plays_all"))\
        .order_by('-views')

    
    result = []
    for row in qresult:
        result.append({
            "user_id": row["video__team__owner__pk"],
            "plan": settings.PLANS.get(row["video__team__owner__subscription__plan"], settings.DEFAULT_PLAN),
            "views": row["views"],
        })
    return result


#
# Notify user that he is going to go over his quota soon
#
def _handle_user_warning(user):
    if user.quota_info.warning_sent:
        return
    user.quota_info.warning_sent = True
    user.quota_info.save()
    mailer.send_mail('quota_warning', {}, user)


#
# Tell user, that he has hit his quota
#
def _handle_user_exceeded(user):
    if user.quota_info.quota_exceeded:
        return
    user.quota_info.quota_exceeded = True
    user.quota_info.save()
    mailer.send_mail('quota_exceeded', {}, user)

