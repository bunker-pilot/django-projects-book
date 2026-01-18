from django.shortcuts import render, redirect,get_object_or_404
from .models import PostModel
from django.urls import reverse_lazy
from django.views.generic import ListView, View
# Create your views here.

class Home(ListView):
    model = PostModel
    template_name = "blog/home.html"
    context_object_name= "new-posts"
    def get_queryset(self):
        super().get_queryset()
        return PostModel.presented.all()[:3]
    
def Posts(request):
    return render(request , "all_posts.html" , {"posts": PostModel.presented.all() })
class PostDetail(View):
    def get(self , request, slug):
        selected_post = get_object_or_404(PostModel , slug = slug)
        return render(request , "blog/post_detail.html" , {"post": selected_post})
    def post(self, request):
        pass
    
def just_get_it(request , id):
    selected_post = get_object_or_404(PostModel , id =id)
    return render(request, "post_detail.html" , {"psot": selected_post})