from django.db import models

class Tag(models.Model):
	name = models.CharField(max_length=60)

	def __unicode__(self):
		return self.name

class Post(models.Model):
	PUB_CHOICES = (
			(u'Y', u'Yes'),
			(u'N', u'No'),
	)
	title = models.CharField(max_length=60)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	is_pub = models.CharField(max_length=2, choices=PUB_CHOICES, verbose_name="published?")
	tags = models.ManyToManyField(Tag)

	def __unicode__(self):
		return self.title

class Comment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	author = models.CharField(max_length=60)
	body = models.TextField()
	post = models.ForeignKey(Post)

	def __unicode__(self):
		return unicode("%s: %s" % (self.post, self.body[:60]))

	def save(self, *args, **kwargs):
		"""Email when a comment is added"""
		if "notify" in kwargs and kwargs["notify"] == True:
			message = "Comment was added to '%s' by '%s': \n\n%s" % (self.post, self.author, self.body)

			from_address = 'noreply@lexandstuff'
			recipient_list = ["lextoumbourou@gmail.com"]
			send_mail("New comment added", message, from_address, recipient_list)

		if "notify" in kwargs: del kwargs["notify"]
		super(Comment, self).save(*args, **kwargs)

### Admin
