from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="images_created", on_delete=models.CASCADE)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_images", blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image =models.ImageField( upload_to="images/%Y/%m/%d/")
    url = models.URLField(max_length=2000)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ] 
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args , **kwargs)
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    