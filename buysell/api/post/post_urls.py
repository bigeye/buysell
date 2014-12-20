from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from buysell.api.post import views

urlpatterns = patterns('',
    url(r'^$', views.PostCreateHandler.as_view()),
    url(r'^list/$', views.PostListHandler.as_view()),
    url(r'^(?P<post_id>\d+)/$', views.PostHandler.as_view()),
    url(r'^(?P<post_id>\d+)/image/$', views.PostImageCreateHandler.as_view()),
    url(r'^(?P<post_id>\d+)/image/(?P<image_id>\d+)/$', views.PostImageHandler.as_view()),
    url(r'^(?P<post_id>\d+)/transaction/$', views.TransactionCreateHandler.as_view()),
    url(r'^(?P<post_id>\d+)/transactions/$', views.TransactionListHandler.as_view()),
    url(r'^(?P<post_id>\d+)/review/$', views.ReviewHandler.as_view()),
)
