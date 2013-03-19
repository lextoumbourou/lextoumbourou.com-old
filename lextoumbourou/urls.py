from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('lextoumbourou.blog.urls')),
    url(r'^$', include('lextoumbourou.blog.urls')),
    url(r'^robots.txt', direct_to_template,
        {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    url(r'^humans.txt', direct_to_template,
        {'template': 'humans.txt', 'mimetype': 'text/plain'}),
)
