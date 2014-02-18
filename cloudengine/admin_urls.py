from django.conf.urls import patterns, url
from cloudengine.core.views import (CreateAppView, 
                AdminHomeView, AppView, AppDataView,
                AppFilesView, AppPushView, AppUsersView,
                AppSettingsView)

urlpatterns = patterns('',

                        url(r'^$', AdminHomeView.as_view(), 
                            name="cloudengine-admin-home"),
                        
                        url(r'^create_app/$', CreateAppView.as_view()),
                        url(r'^apps/(?P<app_name>[a-zA-Z0-9_\-]+)/$', 
                            AppView.as_view(), name="cloudengine-app-view"),
                       
                       url(r'^apps/(?P<app_name>[a-zA-Z0-9_\-]+)/data/$', 
                            AppDataView.as_view(), name="cloudengine-app-data"),
                       
                       url(r'^apps/(?P<app_name>[a-zA-Z0-9_\-]+)/files/$', 
                            AppFilesView.as_view(), name="cloudengine-app-files"),
                       
                       url(r'^apps/(?P<app_name>[a-zA-Z0-9_\-]+)/push/$', 
                            AppPushView.as_view(), name="cloudengine-app-push"),
                       
                       url(r'^apps/(?P<app_name>[a-zA-Z0-9_\-]+)/users/$', 
                            AppUsersView.as_view(), name="cloudengine-app-users"),
                       
                       url(r'^apps/(?P<app_name>[a-zA-Z0-9_\-]+)/settings/$', 
                            AppSettingsView.as_view(), name="cloudengine-app-settings"),
                       )
