from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from buysell.api.post import views

urlpatterns = patterns('',
    url(r'^/$', views.PostCreateHandler.as_view()),
    url(r'^list/$', views.PostListHandler.as_view()),
    url(r'^(?P<post_id>[0-9]*)/$', views.PostHandler.as_view()),
    url(r'^(?P<post_id>[0-9]*)/transaction/$', views.TransactionCreateHandler.as_view()),
    url(r'^(?P<post_id>[0-9]*)/transactions/$', views.TransactionListHandler.as_view()),
    url(r'^(?P<post_id>[0-9]*)/review/$', views.ReviewHandler.as_view()),
)
