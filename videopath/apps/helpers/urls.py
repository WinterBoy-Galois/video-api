from django.conf.urls import url, patterns




urlpatterns = patterns('',

    # reset password
    url(r'^check_url', 'videopath.apps.helpers.views.check_url_view'),

)
