from django.urls import path
from . import views

app_name = "images"
urlpatterns = [
    path("create/" , views.CreateImage.as_view() , name="create"),
    path("detail/<int:id>/<slug:slug>/" , views.image_detail , name="detail"),
    path("like/" , views.ImageLike.as_view() , name="like")
]
