from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegisterationForm
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
    
@login_required
def dashboard(request):
    return render(request , "account/dashboard.html" , {"section":"dashboard"})

#task : added email verification for registeration
class UserRegisteration(View):
    def get(self, request):
        form = UserRegisterationForm()
        return render(request , "account/register.html" , {"form":form})
    def post(self, request):
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            return render(request , "account/register_done.html" , {"new_user":new_user})
        return render(request , "account/register.html" , {"form":form})