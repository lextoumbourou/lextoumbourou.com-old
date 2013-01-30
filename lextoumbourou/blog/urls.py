from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from lextoumbourou.blog.feeds import LatestEntriesFeed
admin.autodiscover()

urlpatterns = patterns('lextoumbourou.blog.views',
    url(r'^filter/tag/(?P<tag_name>[A-Za-z]+)/$', 'filter_by_tag'),
    url(r'^contact', direct_to_template, {'template': 'contact.html'}),
    url(r'^feed/', LatestEntriesFeed()),
    url(r'^$', 'main'),
    url(r'^posts/(.*)/$', 'post'),
)
