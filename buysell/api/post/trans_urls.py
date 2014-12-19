from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from buysell.api.post import views

urlpatterns = patterns('',
    url(r'^(?P<transaction_id>[0-9]*)/$', views.TransactionHandler.as_view()),
    url(r'^(?P<transaction_id>[0-9]*)/message/$', views.MessageCreateHandler.as_view()),
    url(r'^(?P<transaction_id>[0-9]*)/message/list/$', views.MessageListHandler.as_view()),
)
