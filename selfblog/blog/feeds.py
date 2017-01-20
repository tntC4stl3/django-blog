from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from .models import Article


class BlogFeed(Feed):
    title = "tntC4stl3's blog"
    link = "/"

    feed_type = Atom1Feed
    mime_type = 'application/xml'

    def items(self):
        return Article.objects.filter(status=0)

    def item_link(self, item):
        return reverse('blog:detail', args=[item.year, item.month, item.slug])

    def item_pubdate(self, item):
        return item.published_time

    def item_updatedate(self, item):
        return item.updated_time

    def item_author_name(self):
        return "tntC4stl3"
