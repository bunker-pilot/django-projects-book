from django.db import models
from django.utils import timezone
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
    slug = models.SlugField(max_length=250, unique=True)
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

    def __str__(self):
        return self.title
