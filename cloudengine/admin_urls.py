from django.conf.urls import patterns, url, include
from cloudengine.decorators import admin_view
from cloudengine.core.views import (CreateAppView, 
                AdminHomeView, AppView, AppSettingsView)

urlpatterns = patterns('',

                        url(r'^$', admin_view (AdminHomeView.as_view()), 
                            name="cloudengine-admin-home"),
                        
                        url(r'^create_app/$', CreateAppView.as_view()),
                        url(r'^apps/(?P<app_name>[a-zA-Z0-9_\-]+)/$', 
                            AppView.as_view(), name="cloudengine-app-view"),
                       
                       url(r'^classes/', 
                            include('cloudengine.classes.urls')),
                       
                       url(r'^files/', 
                            include('cloudengine.files.urls')),
                       
                       url(r'^push/$', 
                            include('cloudengine.push.urls')),
                       
                       url(r'^users/$', 
                            include('cloudengine.users.urls')),
                       
                       url(r'^apps/(?P<app_name>[a-zA-Z0-9_\-]+)/settings/$', 
                            AppSettingsView.as_view(), name="cloudengine-app-settings"),
                       )
