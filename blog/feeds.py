from django.contrib.syndication.views import Feed
from lexandstuff.blog.models import *

class LatestEntriesFeed(Feed):
	title = 'LexToumbourou.com latest stories'
	link = '/feed/'
	description = 'A blog about coding and other stuff I think the internet should know'

	def items(self):
		return Post.objects.order_by('-created')

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.desc

	def item_link(self, item):
		return 'http://lexandstuff.com/blog/posts/'+item.slug
