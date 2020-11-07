from django.conf.urls import url, patterns

urlpatterns = patterns('',
   url(r'^mails/(?P<mail>[0-9a-z_]+)/(?P<mailtype>(html|txt)+)/', 'videopath.apps.common.mailer.view.mailview'),
   url(r'^mails/', 'videopath.apps.common.mailer.view.view'),
)
