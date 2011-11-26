from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('lexandstuff.blog.views',
	# The tag filter
	url(r'^filter/tag/(?P<tag_name>[A-Za-z]+)/$', 'filter_by_tag'),
	url(r'^contact', direct_to_template, {'template': 'contact.html'}),
	url(r'^about', direct_to_template, {'template': 'about.html'}),
	url(r'^$', 'main'),
	url(r'^posts/(\d+)/$', 'post'),
	url(r'^add_comment/(\d+)/$', 'add_comment'),
)
