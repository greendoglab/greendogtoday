from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^page/(?P<slug>[^\.]+)/$', 'pages.views.page', name='page'),
)
