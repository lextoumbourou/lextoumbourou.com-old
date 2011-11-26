from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.syndication.views import Feed
from calendar import month_name
import time
from lexandstuff.blog.models import *

def main(request):
	"""Main listing."""

	# Get all posts order by created date (desc)
	posts = Post.objects.all().order_by("-created")

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

	return render_to_response("list_articles.html", dict(posts=posts, user=request.user, post_list=posts.object_list))

def post(request, pk):
	"""Single post with comments and comment form"""

	# Get a single post
	post = Post.objects.get(pk=int(pk))

	# Get all the comments for that post
	comments = Comment.objects.filter(post=post)
	d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)

	# Keep data same from cross-site scripting
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

