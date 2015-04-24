from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^post/(?P<slug>[^\.]+)/$', 'blog.views.post', name='post'),
    url(r'^tag/(?P<slug>[^\.]+)/$', 'blog.views.tag', name='tag'),
)
