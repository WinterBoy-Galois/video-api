from django.conf.urls import url, patterns


urlpatterns = patterns('',


   #
   # image file uploads
   #
   url(r'^image/upload/requestticket/(?P<type>.+)/(?P<related_id>[0-9]+)/$', 'videopath.apps.files.views.image_request_upload_ticket'),
   url(r'^image/upload/complete/(?P<ticket_id>.+)/$', 'videopath.apps.files.views.image_upload_complete'),

)


