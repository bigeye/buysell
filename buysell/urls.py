from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'buysell.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'buysell.apps.home.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('buysell.api.urls')),
    url(r'^register/', 'buysell.apps.home.views.register'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
