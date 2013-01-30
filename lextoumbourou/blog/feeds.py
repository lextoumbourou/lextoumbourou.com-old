from django.contrib.syndication.views import Feed
from lextoumbourou.blog.models import *


class LatestEntriesFeed(Feed):
    title = 'LexToumbourou.com latest stories'
    link = '/feed/'
    description = (
        'A blog about coding and other stuff I think the internet should know')

    def items(self):
        return (Post.objects.exclude(type='I')
                            .filter(is_pub='Y')
                            .order_by('-created'))

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return 'http://lextoumbourou.com/blog/posts/'+item.slug
