from django.shortcuts import render, redirect,get_object_or_404
from .models import PostModel
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

class Home(ListView):
    model = PostModel
    template_name = "blog/home.html"
    context_object_name= "new-posts"
    queryset= PostModel.presented.all()[:3]
class Posts(ListView):
    template_name = "blog/all_posts.html"
    model = PostModel
    queryset = PostModel.presented.all()
    paginate_by = 5
    context_object_name = "posts"
"""   
def Posts(request):
    post_lists = PostModel.published.all()
    paginator = Paginator(post_lists , 5)
    page_number = request.GET.get("page" , 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request , "all_posts.html" , {"posts": posts })
"""
class PostDetail(View):
    def get(self , request, slug , day,year,month):
        selected_post = get_object_or_404(
            PostModel ,status= PostModel.Status.Published, slug = slug, published__day=day
            ,published__month = month , published__year=year
            )
        return render(request , "blog/post_detail.html" , {"post": selected_post})
    def post(self, request):
        pass
    
def just_get_it(request , id):
    selected_post = get_object_or_404(PostModel , id =id)
    return render(request, "blog/post_detail.html" , {"psot": selected_post})