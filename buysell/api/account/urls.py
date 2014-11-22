from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from buysell.api.account import views

urlpatterns = patterns('',
    url(r'^user$', views.UserHandler.as_view()),
    url(r'^login$', views.SessionLoginHandler.as_view()),
    url(r'^logout$', views.SessionLogoutHandler.as_view()),
    url(r'^auth_token$', views.JWTLoginHandler.as_view()),
    url(r'^notification$$', views.NotificationHandler.as_view()),
    url(r'^transaction$$', views.TransactionListHandler.as_view()),

)

urlpatterns = format_suffix_patterns(urlpatterns)
