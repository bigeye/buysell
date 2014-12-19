from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'buysell.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^account/', include('buysell.api.account.urls')),
    url(r'^post/', include('buysell.api.post.post_urls')),
    url(r'^transaction/', include('buysell.api.post.trans_urls')),
)
