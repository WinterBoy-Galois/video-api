from django.conf.urls import url, patterns, include

from rest_framework import routers

from videopath.apps.videos.views import MarkerViewSet, MarkerContentViewSet, VideoViewSet, VideoRevisionViewSet
from videopath.apps.videos.views import video_publish, get_revision, send_share_mail, jpg_sequence_view
from videopath.apps.videos.views import icon_view, thumbnail_view

# Register view sets
router = routers.DefaultRouter()
router.register(r'video/(?P<vid>[0-9]+)/revision', VideoRevisionViewSet, base_name="video_revision")
router.register(r'video/(?P<vid>[0-9]+)/video-revision', VideoRevisionViewSet, base_name="video_revision") # correced alias

router.register(r'video-revision/(?P<vid>[0-9]+)/marker', MarkerViewSet, base_name="marker")

router.register(r'marker/(?P<mid>[0-9]+)/content', MarkerContentViewSet, base_name="marker_content")
router.register(r'marker/(?P<mid>[0-9]+)/marker-content', MarkerContentViewSet, base_name="marker_content") # corrected alias

router.register(r'marker', MarkerViewSet, base_name="marker")
router.register(r'video', VideoViewSet, base_name="video")
router.register(r'team/(?P<team_id>[0-9]+)/video', VideoViewSet, base_name="video")
router.register(r'video-revision', VideoRevisionViewSet, base_name="video_revision")

router.register(r'markercontent', MarkerContentViewSet, base_name="marker_content")
router.register(r'marker-content', MarkerContentViewSet, base_name="marker_content") # corrected alias

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',   

   # special urls that overwrite the Viewsets
   url(r'^video/(?P<vid>[0-9]+)/revision/(?P<rev_type>draft|published)/$', get_revision),
   url(r'^video/(?P<vid>[0-9]+)/video-revision/(?P<rev_type>draft|published)/$', get_revision), # corrected alias

   # publish / unpublish actions
   url(r'^video/(?P<vid>[0-9]+)/public/$', video_publish),

   # send share email
   url(r'^video/(?P<vid>[0-9]+)/share-email/$', send_share_mail),

   # file uploads, icon and thumbnail respectively
   url(r'^video-revision/(?P<rid>[0-9]+)/icon', icon_view),
   url(r'^video-revision/(?P<rid>[0-9]+)/thumbnail', thumbnail_view),

   # source operations
   url(r'^video-revision/(?P<rid>[0-9]+)/source/jpg_sequence/$', jpg_sequence_view),
   url(r'^video-revision/(?P<rid>[0-9]+)/source/jpg-sequence/$', jpg_sequence_view), # corrected alias

   #
   # video source import
   #
   url(r'^video/(?P<key>[0-9]+)/import_source/$','videopath.apps.videos.views.import_source'),
   url(r'^video/(?P<key>[0-9]+)/import-source/$','videopath.apps.videos.views.import_source'), # corrected alias

   #
   # external notifications (for from aws)
   #
   url(r'^notifications/transcode/(?P<type>.+)/$', 'videopath.apps.videos.video_file_views.process_notification'),

   #
   # video file uploads
   #
   url(r'^video/upload/requestticket/(?P<video_id>[0-9]+)/$', 'videopath.apps.videos.video_file_views.video_request_upload_ticket'),
   url(r'^video/upload/request-ticket/(?P<video_id>[0-9]+)/$', 'videopath.apps.videos.video_file_views.video_request_upload_ticket'), # corrected alias
   url(r'^video/upload/complete/(?P<ticket_id>.+)/$', 'videopath.apps.videos.video_file_views.video_upload_complete'),

   # regular api urls
   url(r'', include(router.urls)),
)