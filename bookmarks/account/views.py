from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.views import View


# Create your views here.



class UserLogin(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request , username = cd["username"] , password = cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request , user)
                    return HttpResponse("Login successful")
                return HttpResponse("Account is not active")
            return HttpResponse("Invalid Login")    
    def get(self, request):
        form = LoginForm()
        return render(request , "account/login.html" , {"form":form})