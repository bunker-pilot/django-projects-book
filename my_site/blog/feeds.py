import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars_html
from django.urls import reverse_lazy
from .models import PostModel

class LatestPostsFeed(Feed):

    title = "Deadlog"
    link = reverse_lazy("blog:all_posts")
    description = "Latest Posts"

    def items(self):
        return PostModel.presented.all()[:3]
    
    def items_title(self, item):
        return item.title()
    
    def item_description(self, item):
        return truncatechars_html(markdown.markdown(item.content) , 30)
    
    def item_pubdate(self, item):
        return item.published
