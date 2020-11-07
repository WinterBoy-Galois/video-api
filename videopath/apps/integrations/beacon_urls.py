from django.conf.urls import url, patterns

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.

urlpatterns = patterns('',   

   # oauth endpoint
   url(r'^mailchimp/', 'videopath.apps.integrations.services.mailchimp.views.beacon'),

)