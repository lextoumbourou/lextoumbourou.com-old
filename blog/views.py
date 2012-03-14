from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.syndication.views import Feed
from calendar import month_name
import time
import random
from lexandstuff.blog.models import *
from lexandstuff.blog.forms import *

def main(request):
	"""Main listing."""

	# Get all posts, excluding Info and Unpublished, order by created date (desc)
	posts = Post.objects.all().exclude(type='I').exclude(is_pub='N').order_by("-created")

	# Setup paginator
	paginator = Paginator(posts, 20)

	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try:
		posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)

	return render_to_response("articles.html", dict(posts=posts, user=request.user, slogan=get_slogan(), post_list=posts.object_list))

def post(request, slug, error=None):
	"""Single post with comments and comment form"""

	# Get a post
	post = Post.objects.get(slug=str(slug))

	# Hide the comments and create date if 'info' page
	hide = {}
	if post.type == 'I':
		hide['comments'] = True
		hide['date'] = True

	# Get all comments
	#comments = Comment.objects.filter(post=post)

	d = dict(post=post, slogan=get_slogan(), hide=hide, user=request.user, error=error)

	# Keep data safe
	d.update(csrf(request))

	return render_to_response("post.html", d)

def filter_by_tag(request, tag_name):
	"""Show just the blogs that match a single tag"""

	# Get just the blogs that match the case-insensitive string
	posts = Post.objects.filter(tags__name__iexact=tag_name)

	paginator = Paginator(posts, 6)

	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try:
		posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)

	return render_to_response("list_articles.html", dict(posts=posts, user=request.user, post_list=posts.object_list))

def get_slogan():
	slogs = []
	slogs.append('A blog about coding and other stuff I think the internet should know')
	slogs.append('The story of a guy with a long last name')
	slogs.append('Automation, XBMC, Python, fun and fulfillment')
	slogs.append('Don\'t feel bad, I probably wouldn\'t read this blog either')

	return slogs[random.randrange(0, len(slogs), 1)]

