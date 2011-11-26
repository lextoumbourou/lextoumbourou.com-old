from django import template
register = template.Library()

from lexandstuff.blog.models import *

@register.inclusion_tag('sidebar/tags.html')
def blog_tags():
	"""Returns all tags as a list"""
	return {
			'tags': Tag.objects.all()
	}

@register.inclusion_tag('sidebar/recent.html')
def blog_recent():
	"""Return all recent post titles"""
	return {
		'posts': Post.objects.order_by("-created")[:6]
	}
