from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ImageForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Image
from django.views.generic import View

# Create your views here.


class CreateImage(LoginRequiredMixin , View):
    def get(self, request):
        form = ImageForm(data = request.GET)
        return render(request , "images/image/create.html" , {"form":form , "section":"images"} )
    def post(self, reuqest):
        form = ImageForm(data = reuqest.POST) 
        if form.is_valid():
            cd = form.cleaned_data
            new_image= form.save(commit = False)
            new_image.user = reuqest.user
            new_image.save()
            messages.success(reuqest , "Image added successfuly")
            return redirect(new_image.get_absolute_url())
        return render(reuqest , "images/image/create.html" , {"form":form,"section":"images"})
    


def image_detail(request , id, slug):
    image = get_object_or_404(Image , pk = id , slug =slug)
    return render(request , "images/image/detail.html" , {"section":"images" , "image": image})