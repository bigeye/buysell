from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from buysell.api.post import views

urlpatterns = patterns('',
    url(r'^$', views.PostListHandler.as_view()),
    url(r'^(?P<post_id>[0-9]*)/$', views.PostHandler.as_view()),
    # user aspect url
    url(r'^(?P<post_id>[0-9]*)/transaction/$', views.TransactionHandler.as_view()),
    url(r'^(?P<post_id>[0-9]*)/transaction/review/$', views.ReviewHandler.as_view()),
    url(r'^(?P<post_id>[0-9]*)/transaction/message/$', views.MessageHandler.as_view()),
)
