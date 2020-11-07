import collections
import humanize
from datetime import date, timedelta
from videopath.apps.users.models import User
from django.utils.encoding import smart_text
from random import choice
from string import ascii_uppercase
from json import dumps

base = "/admin/insights/"

company_accounts = [
        "david",
        "product_demo", #company
        "marketing", # company
        "anna",
        "tim t", #tim 2
        "tim", # tim 1
        "trival", # thomas
        "nimaa", 
        "lcdenison", # louisa 1
        "dontdelete", # louisa 2
        "yana",
        "jolly",
        "junayd",
        "vp_test_basic",
        "vp_test_pro",
        "vp_test_enterprise",
]

def header(text):
    return "<h3>" + text + "</h3>"

def table(array, header = None):
    
    result = ""
    if header:
        result = "<tr>"
        for item in header:
            result += "<th>" + smart_text(item) + "</th>"
        result += "</tr>"

    for row in array:
        rowr = "<tr>"
        for item in row:
            rowr += "<td>" +smart_text(item) + "</td>"
        result += rowr + "</tr>"

    return "<table>" + result + "</table>"

def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

def videolink(v):
    detail_url = base + "videos/" + v.key + "/"
    revision = None
    try:
        revision = v.draft
    except:
        return None
    return [
        "<a href ='" + detail_url + "'>" + smart_truncate(revision.title, 50) + "</a>",
        v.team.owner.username,
        humanize.naturalday(revision.modified),
        str(v.total_plays) 
    ] 

def videolist(videos):
    result_array = []
    for video in videos:
        link = videolink(video)
        if link:
            result_array.append(link)
    return table(result_array, ["Title", "User", "Modified", "Plays"])


def userlink(user):
    username = user.username if isinstance(user, User) else user
    url = base + 'users/' + username +"/"
    return "<a href = '"+url+"'>"+username+"</a>"

def chart(values, t):
    result = ''

    key = (''.join(choice(ascii_uppercase) for i in range(12)))
    result += "<div class='vp_linegraph' id='{0}'></div>".format(key)

    types= {
        'line': 'LineChart',
        'pie': 'PieChart',
        'column': "ColumnChart"
    }

    options = {
        "curveType": "function",
        "colors": ['#81b9c3','#41c3ac','#ff884d', '#ff6b57', '#273a45', '#c6c6c6', '#f8f8f8'],
        "legend": { "position": "in"},
        "vAxis": {
            "viewWindow": {
                "min": 0
            }
        },
        "pointSize": 3
    }

    result += (
        "<script type='text/javascript'>"
        "google.charts.setOnLoadCallback({0});"
        "function {0}() {{"

            "var data = google.visualization.arrayToDataTable({1});"

            "var options = {2};"
            "var chart = new google.visualization.{3}(document.getElementById('{0}'));"
            "chart.draw(data, options);"
        "}}"
        "</script>"
    ).format(key, dumps(values), dumps(options), types[t])

    return result


#
# Build weekly date graph
#
def dategraph(models, datefield, accumulate=False, aggregate_field = None, metric_name='name'):

    timestring = "%G %V"

    # build dict
    values = {}
    for model in models:
        value = getattr(model, datefield)
        key = value.strftime(timestring)

        count = 1
        if aggregate_field:
            count = getattr(model, aggregate_field)

        values[key] = values.get(key, 0) + count

    datecount = date(2014,1,1)
    while datecount < date.today():
        datecount += timedelta(days=7)
        key = datecount.strftime(timestring)
        values[key] = values.get(key, 0)

    # sort
    values = collections.OrderedDict(sorted(values.items()))

    # accumulate if needed
    if accumulate:
        total = 0
        for key in values:
            total = total + values[key]
            values[key] = total

    return chart([['week', metric_name]] + values.items(), 'line')





