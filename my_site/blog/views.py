from django.shortcuts import render, redirect,get_object_or_404
from .models import PostModel
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST #makes a view to only be used for post requests and it will throw an http 405(mehtod not allowed) otherwise
from django.views.generic import ListView, View
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count, Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
# Create your views here.

class Home(ListView):
    model = PostModel
    template_name = "blog/home.html"
    context_object_name= "newposts"
    queryset= PostModel.presented.all()[:3]
class Posts(ListView):
    template_name = "blog/all_posts.html"
    model = PostModel
    queryset = PostModel.presented.all()
    paginate_by = 5
    context_object_name = "posts"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get("tag_slug" , False)
        if tag_slug:
            context["tag"] = get_object_or_404(Tag , slug =tag_slug )
            context["posts"] = PostModel.presented.filter(tags__in=[context["tag"]])
        return context
    

    
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
        #similar posts based on the tags
        post_tags = selected_post.tags.values_list("id",flat=True)
        similar_posts = PostModel.presented.filter(tags__in=post_tags).exclude(id = selected_post.id)
        similar_posts = similar_posts.annotate(same_tags = Count("tags" , filter=Q(tags__in=post_tags))).order_by("-same_tags" , "-published")[:2]
        comments = selected_post.comments.filter(active = True)
        return render(request , "blog/post_detail.html" , {
            "post": selected_post , "form":form , "similar_posts":similar_posts,
            "comments":comments})

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
            return redirect("blog:post_detail", slug=slug,day=day,year=year,month=month)
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
            subject = (f"{cd["name"]} : {cd["email"]}"
                       f"recommended for you: {post.title}")
            message= (f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comment: {cd['comments']}")
            send_mail(
                subject=subject,
                message=message,
                recipient_list=[cd["to"]]
            )
            sent= True
        else:
            sent =False
        return render(request , "blog/share.html" , {"post": post, "form": form , "sent":sent})
def just_get_it(request , id):
    selected_post = get_object_or_404(PostModel , id =id)
    return render(request, "blog/post_detail.html" , {"post": selected_post})


class PostSerach(View):
    def get(self, request):
        form = SearchForm()
        return render(request , "blog/search.html" , {"form":form})
    def post(self , request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            #search_query = SearchQuery(query)
            #search_vector = SearchVector("title", weight="A") + SearchVector("content" , weight="B")
            #results = (PostModel.presented.annotate(search =search_vector , rank = SearchRank(search_vector , search_query)).filter(rank__gte = 0.3).order_by("-rank"))
            results = PostModel.presented.annotate(similarity = TrigramSimilarity("title" , query)).filter(similarity__gt=0.1).order_by("-similarity")
            return render(request , "blog/search.html" , {"form" : form ,"query":query , "results":results})
        return render(request , "blog/search.html" , {"form":form})