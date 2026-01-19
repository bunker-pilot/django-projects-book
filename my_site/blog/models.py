from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=PostModel.Status.Published)
class PostModel(models.Model):
    objects = models.Manager()# the defaul manager
    presented = PublishedManager() # the custom manager
    
    class Status(models.TextChoices):
        Draft = "DF" , "Draft"
        Published = "PB" , "Published"
    title = models.CharField(max_length=300)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date="published")
    image = models.ImageField(upload_to="posts/")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name="blog_posts")
    published = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField( choices=Status, default=Status.Draft, max_length=2)
    class Meta:
        verbose_name = "posts"
        ordering= ["-published"]
        
        indexes = [
            # could have just used db_index=True in the published field, but it doesn't index in decending order
            models.Index(fields=[("-published")]) 
        ]

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={
            "slug": self.slug ,"day":self.published.day 
            ,"month":self.published.month, "year": self.published.year
            })
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey( PostModel, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    body = models.TextField(max_length=400)
    created = models.DateTimeField( auto_now_add=True)
    updated = models.DateTimeField( auto_now=True)
    active = models.BooleanField(default=True)

    class Meata:
        ordering= ["craeted"]
        indexes = [models.Index(fields=[("created")])]
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"