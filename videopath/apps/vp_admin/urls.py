from django.conf.urls import url, patterns

urlpatterns = patterns('',
   
   url(r'^insights/kpis-cohort/', 'videopath.apps.vp_admin.views.kpis-cohort.view'),
   url(r'^insights/kpis-all/', 'videopath.apps.vp_admin.views.kpis-all.view'),
   url(r'^insights/kpis-web/', 'videopath.apps.vp_admin.views.kpis-web.view'),
   url(r'^insights/users/sales/', 'videopath.apps.vp_admin.views.users.listview_sales'),
   url(r'^insights/users/(?P<username>.+)/', 'videopath.apps.vp_admin.views.users.userview'),
   url(r'^insights/users/', 'videopath.apps.vp_admin.views.users.listview'),

   url(r'^insights/subscriptions/', 'videopath.apps.vp_admin.views.subscriptions.view'),

   url(r'^insights/userstats/', 'videopath.apps.vp_admin.views.userstats.view'),
   
   url(r'^insights/videos/(?P<key>.+)/', 'videopath.apps.vp_admin.views.videos.videoview'),
   url(r'^insights/videos/', 'videopath.apps.vp_admin.views.videos.listview'),

   url(r'^insights/features/', 'videopath.apps.vp_admin.views.features.view'),


   url(r'^insights/billing/', 'videopath.apps.vp_admin.views.billing.view'),
   url(r'^insights/', 'videopath.apps.vp_admin.views.base.view'),

   # exports
   url(r'^sales/inbound-users/', 'videopath.apps.vp_admin.views.sales.inbound_users'),

   # url for external health check
   url(r'^YT58Pc3u6ZlK/health/', 'videopath.apps.vp_admin.views.health_check.view'),

)


#from django.contrib.admin.views.decorators import staff_member_required
