from django.conf.urls import patterns, url, include
from core.views import AppView, AppListView

urlpatterns = patterns('',

                       url(r'^classes/', include('classes.api_v1_urls')),
                       url(r'^files/', include('files.api_v1_urls')),
                       url(r'^push/', include('push.api_v1_urls')),
                       url(r'^apps/(?P<name>[a-zA-Z0-9]+)/$',
                           AppView.as_view()),
                       url(r'^apps/$', AppListView.as_view())
                       )
