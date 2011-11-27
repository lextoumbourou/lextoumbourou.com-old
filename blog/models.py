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

	def __unicode__(self):
		return self.title

class Comment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	author = models.CharField(max_length=60)
	body = models.TextField()
	post = models.ForeignKey(Post)

	def __unicode__(self):
		return unicode("%s: %s" % (self.post, self.body[:60]))

### Admin
