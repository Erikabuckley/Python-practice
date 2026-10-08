from django.contrib.syndication.views import Feed
from django.urls import reverse

from forum.models import Post

class LatestPostFeed(Feed):
    title = 'Out Posts'
    link = '/latest/posts'
    description = 'latest posts'
    
    def items(self):
        return Post.objects.order_by('-created_at')[:5]
    
    def item_title(self, item):
        return item.title
        
    def item_description(self, item):
        return item.body
        
    def item_link(self, item):
        return reverse('detail', args=[item.pk])
    
    