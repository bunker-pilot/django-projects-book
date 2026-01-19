from django.shortcuts import render, redirect,get_object_or_404
from .models import PostModel
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST #makes a view to only be used for post requests and it will throw an http 405(mehtod not allowed) otherwise
from django.views.generic import ListView, View
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm, CommentForm
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
        form = CommentForm()
        selected_post = get_object_or_404(
            PostModel ,status= PostModel.Status.Published, slug = slug, published__day=day
            ,published__month = month , published__year=year
            )
        comments = selected_post.commments.filter(active = True)
        return render(request , "blog/post_detail.html" , {"post": selected_post , "form":form , "comments":comments})
    def post(self, request ,  slug , day,year,month):
        form = CommentForm(request.POST)
        selected_post = get_object_or_404(
            PostModel ,status= PostModel.Status.Published, slug = slug, published__day=day
            ,published__month = month , published__year=year
            )
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = selected_post
            comment.save()
            return redirect("post_detial" , args = [slug , day , year, month])
        return render(request , "blog/post_detail.html" , {
            "post" :selected_post , 
            "form" : form,
            "comments" : selected_post.comments.all()
        })
class SharePost(View):
    def get(self, request , id):
        post = get_object_or_404(PostModel , id =id , status= PostModel.Status.Published )
        form = EmailPostForm()
        sent = False
        return render(request , "blog/share.html" , {"post": post, "form": form , "sent":sent})
    def post(self, request , id):
        post = get_object_or_404(PostModel , id =id , status= PostModel.Status.Published )
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{cd["name"]}  {cd["email"]}"
                       f"recommended for you: {post.title}")
            message= (f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comment: {cd['comments']}")
            send_mail(
                subject=subject,
                message=message,
                recipient_list=[cd["to"]]
            )
            sent= True
        return render(request , "blog/share.html" , {"post": post, "form": form , "sent":sent})
def just_get_it(request , id):
    selected_post = get_object_or_404(PostModel , id =id)
    return render(request, "blog/post_detail.html" , {"psot": selected_post})