from django.template import Library
from ..models import PostModel
from django.db.models import Count

register = Library()

# django will register the function name as the tag name
#if you want a custom name ==> @register.simple_tag(name="my_tag")
@register.simple_tag
def total_posts():
    return PostModel.presented.count()

@register.inclusion_tag("blog/latest_posts.html")
def show_latest_posts(count = 4):
    latest_posts = PostModel.presented.order_by("-published")[:count]
    return {"latest_posts": latest_posts}

@register.simple_tag
def most_commented_posts(count = 3):
    return PostModel.presented.annotate(most_comments = Count("comments")).order_by("-most_comments")[:count]