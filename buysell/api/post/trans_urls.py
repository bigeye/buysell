from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from buysell.api.post import views

urlpatterns = patterns('',
    url(r'^(?P<transaction_id>\d+)/message/$', views.MessageCreateHandler.as_view()),
    url(r'^(?P<transaction_id>\d+)/message/list/$', views.MessageListHandler.as_view()),
)
