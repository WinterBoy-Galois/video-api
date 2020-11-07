
from .decorators import group_membership_required
from django.template.response import SimpleTemplateResponse

from videopath.apps.vp_admin.views import helpers
from videopath.apps.payments.models import Subscription
from django.conf import settings
import humanize


@group_membership_required('insights')
def view(request):

    # collect subscriptions
    result_array = []
    for sub in Subscription.objects.all().order_by("plan"):
        if sub.plan != settings.DEFAULT_PLAN["id"] and sub.user.username not in helpers.company_accounts:
            result_array.append([
                    helpers.userlink(sub.user),
                    sub.plan,
                    sub.managed_by,
                    sub.notes
                ])
    headers = ["User", "Plan", "Payment Method", "Notes"]
    result = helpers.table(result_array, headers)

    result += helpers.header("Plans")


    # collect Plans
    def renderplan( plan):
        features = ""
        for key, value in plan.iteritems():
            if "feature" in key:
                feature = key.replace("feature_", "") 
                if value:
                    feature =  feature 
                else:
                    feature = "<span style='color:lightgray'>" + feature + "</span>"
                features += feature + "  "
 
        result = [ "<b>" + plan["name"] + "</b><br />" + plan["id"], 
        humanize.intcomma(plan["price_usd"]/100), 
        humanize.intcomma(plan["price_eur"]/100), 
        humanize.intcomma(plan["price_gbp"]/100),         
        plan['payment_interval'],
        features,
        "x" if plan["subscribable"] else "",
        "x" if plan["listable"] else "",
        Subscription.objects.filter(plan=plan['id']).count()]
        return result

    array = []    
    for plan in settings.PLANS_SORTED:
        array.append(renderplan(plan))
    result += helpers.table(array, ["Name", "USD", "EUR", "GBP", "Interval", "Features", "Subs.", "Listable", "No. Users"])


    return SimpleTemplateResponse("insights/base.html", {
        "title": "Subscriptions and Plans",
        "insight_content": result
        })
