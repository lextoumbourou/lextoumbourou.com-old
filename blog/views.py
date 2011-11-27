from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.syndication.views import Feed
from calendar import month_name
import time
import random
from lexandstuff.blog.models import *

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

def post(request, pk):
	"""Single post with comments and comment form"""

	# Get a post
	post = Post.objects.get(pk=int(pk))

	# Hide the comments and create date if 'info' page
	hide = {}
	if post.type == 'I':
		hide['comments'] = True
		hide['date'] = True

	# Get all comments
	comments = Comment.objects.filter(post=post)

	d = dict(post=post, slogan=get_slogan(), comments=comments, hide=hide, form=CommentForm(), user=request.user)

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

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ["post"]

def add_comment(request, pk):
	"""Add a new comment"""
	p = request.POST

	if p.has_key("body") and p["body"]:
		author = "Anonymous"
		if p["author"]: author = p["author"]

		comment = Comment(post=Post.objects.get(pk=pk))
		cf = CommentForm(p, instance=comment)
		cf.fields["author"].required = False

		comment = cf.save(commit=False)
		comment.author = author
		comment.save()
	
	return HttpResponseRedirect(reverse("lexandstuff.blog.views.post", args=[pk]))

def get_slogan():
	slogs = []
	slogs.append('A blog about coding and other stuff I think the internet should know.')
	slogs.append('The wonderful blog of Lex Toumbouou.')
	slogs.append('Automation, XBMC, Python, fun and fulfillment.')

	return slogs[random.randrange(0, 3, 1)]

