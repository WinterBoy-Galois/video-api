from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# always redirect to admin from base url
	url(r'^$', RedirectView.as_view(url='admin/')),

	# users app
	url(r'^v1/', include('videopath.apps.users.urls')),

	# files app
	url(r'^v1/', include('videopath.apps.files.urls')),

	# payments app
	url(r'^v1/', include('videopath.apps.payments.urls')),

	# analytics app
	url(r'^v1/', include('videopath.apps.analytics.urls')),

	# videos app, needs to be last to catch all the remaining video requests
	url(r'^v1/', include('videopath.apps.videos.urls')),

	url(r'^helpers/', include('videopath.apps.helpers.urls')),

	# oembed is in videos app for now
	url(r'^oembed/', 'videopath.apps.videos.views.oembed'),

	# integrations urls
	url(r'^oauth/', include('videopath.apps.integrations.oauth_urls')),
	url(r'^v1/beacon/', include('videopath.apps.integrations.beacon_urls')),
	url(r'^v1/', include('videopath.apps.integrations.urls')),

	# admin urls
	url(r'^admin/', include('videopath.apps.vp_admin.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^grappelli/', include('grappelli.urls')),

	# rest framework
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

	url(r'^qa/', include('videopath.apps.common.urls')),

	# some public urls
	url(r'^public/invoices/(?P<invoice_id>[0-9]+)', 'videopath.apps.payments.views.public_invoice'),
)



