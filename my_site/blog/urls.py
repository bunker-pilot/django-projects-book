from django.urls import path
from . import views

app_name= "blog"
urlpatterns = [
    path("" , views.Post_list.as_view() , name = "hoome"),
    path("<slug:slug>/" , views.PostDetail.as_view(), name ="post_detail"),
    path("<int:id>/" , views.just_get_it , name = "justgetit")
]

#task = learn how to use the custom model manager with Class based views, and make a "all blogs" page