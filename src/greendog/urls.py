from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from greendog.views import AllFeed

urlpatterns = patterns(
    '',
    url(r'^$', 'greendog.views.HomeView', name='home'),

    url(r'^', include('blog.urls')),
    url(r'^', include('pages.urls')),

    url(r'^feed/$', AllFeed()),

    # url(r'^redactor/', include('redactor.urls')),
    (r'^media/(.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', 'greendog.views.SearchView', name='search')
)
