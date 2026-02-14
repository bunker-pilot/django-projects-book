from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ImageForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import HttpResponse, Http404
from django.core.paginator import EmptyPage
from django.views.generic import View, ListView
from django.http import JsonResponse

# Create your views here.


class CreateImage(LoginRequiredMixin , View):
    def get(self, request):
        form = ImageForm(data = request.GET)
        return render(request , "images/image/create.html" , {"form":form , "section":"images"} )
    def post(self, request):
        form = ImageForm(data = request.POST) 
        if form.is_valid():
            cd = form.cleaned_data
            new_image= form.save(commit = False)
            new_image.user = request.user
            new_image.save()
            messages.success(request , "Image added successfuly")
            return redirect(new_image.get_absolute_url())
        return render(request , "images/image/create.html" , {"form":form,"section":"images"})
    


def image_detail(request , id, slug):
    image = get_object_or_404(Image , pk = id , slug =slug)
    return render(request , "images/image/detail.html" , {"section":"images" , "image": image})



class ImageLike(LoginRequiredMixin , View):
    def post(self, request):
        image_id = request.POST.get("id")
        action = request.POST.get("action")
        if image_id and action:
            try:
                image= Image.objects.get(pk = image_id)
                if action =="like":
                    image.users_like.add(request.user)
                else:
                    image.users_like.remove(request.user)
                return JsonResponse({"status": "ok"})
            except Image.DoesNotExist:
                pass
        return JsonResponse({"status": "error"})
            

class ImageList(LoginRequiredMixin, ListView):
    template_name = "images/image/list.html"
    model = Image
    context_object_name ="images"
    paginate_by = 8
    queryset = Image.objects.all()
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["section"] = "images"
        return context
    def get_template_names(self):
        if self.request.GET.get("images_only"):
            return ["images/image/list_images.html"]
        return [self.template_name]
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:# task, when paginator tries an empty page, listview turns it into a Http404 error, customize the paginator subclass :)
            if request.GET.get("images_only"):
                return HttpResponse("", status=204)
            return HttpResponse("", status=204)