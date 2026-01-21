from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Profile
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegisterationForm, EditProfileForm,UserEditForm
from django.views import View
from django.contrib import messages


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
            Profile.objects.create(user = new_user)
            return render(request , "account/register_done.html" , {"new_user":new_user})
        return render(request , "account/register.html" , {"form":form})
    

class Edit(LoginRequiredMixin,View ):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
        return render(request , "account/edit_profile.html" , {"user_form" :user_form , "profile_form":profile_form})
    def post(self , request):
        user_form = UserEditForm(data=request.POST , instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile , data=request.POST , files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request , "Profile updated successfuly!")
        else:
            messages.error(request , "Invalid inputs")
        return render(request , "account/edit_profile.html" , {"user_form":user_form,"profile_form":profile_form})
        

