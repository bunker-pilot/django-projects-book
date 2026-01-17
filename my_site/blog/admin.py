from django.contrib import admin
from .models import PostModel

# Register your models here.


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("title",)}
    list_display = ["title" , "published" , "status" , "author"]
    list_filter = ["created_at","updated_at" , "status" , "author"]
    search_fields = ["title" , "content"]
    raw_id_fields = ["author"]
    date_hierarchy = "published"
    ordering = ["status" , "published"]
