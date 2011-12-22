from django.db import models
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.sites.models import Site
from django.conf import settings

class Tag(models.Model):
	name = models.CharField(max_length=60)

	def __unicode__(self):
		return self.name

class Post(models.Model):
	PUB_CHOICES = (
			(u'Y', u'Yes'),
			(u'N', u'No'),
	)
	TYPE_CHOICES = (
			(u'P', u'Project'),
			(u'B', u'Blog'),
			(u'I', u'Info'),
	)
	title = models.CharField(max_length=60)
	slug = models.SlugField(max_length=50)
	desc = models.CharField(max_length=100)
	body = models.TextField()
	created = models.DateField(auto_now=False,auto_now_add=False)
	type = models.CharField(max_length=3)
	is_pub = models.CharField(max_length=2, choices=PUB_CHOICES, verbose_name="published?")
	tags = models.ManyToManyField(Tag)
	enable_comments = models.BooleanField()

	def __unicode__(self):
		return self.title

class PostModerator(CommentModerator):
	def check_spam(self, request, comment, key, blog_url=None, base_url=None):
		'''
		Based on Samuel Cormier-Iijima's code.
		http://sciyoshi.com/2009/7/prevent-django-newcomments-spam-akismet-reloaded/
		'''
		try:
			from akismet import Akismet
		except:
			return False

		if blog_url is None:
			blog_url = 'http://%s/' % Site.objects.get_current().domain

		ak = Akismet(
				key=settings.AKISMET_API_KEY,
				blog_url=blog_url
				)

		if base_url is not None:
			ak.baseurl = base_url

		if ak.verify_key():
			data = {
					'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
					'user_agent': request.META.get('HTTP_USER_AGENT', ''),
					'referrer': request.META.get('HTTP_REFERER', ''),
					'comment_type': 'comment',
					'comment_author': comment.user_name.encode('utf-8'),
					}

			if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
				return True

		return False

	def allow(self, comment, content_object, request):
		allow = super(PostModerator, self).allow(comment, content_object, request)

		spam = self.check_spam(
						request, 
						comment,
						key=settings.AKISMET_API_KEY
						)

		return spam and allow

	email_notification = True
	enable_field = 'enable_comments'

moderator.register(Post, PostModerator)
