from django.shortcuts import render , get_object_or_404 , redirect
from .models import Profile
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegisterationForm, EditProfileForm,UserEditForm
from django.views.generic import View, ListView
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes , force_str
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
# Create your views here.

User = get_user_model()

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
            new_user.is_active = False
            new_user.save()

            current_sit = get_current_site(request)
            subject= "Verify your email"
            message = render_to_string("registration/email_verification.html" , {
                "user": new_user,
                "domain": current_sit.domain,
                "uid": urlsafe_base64_encode(force_bytes(new_user.id)),
                "token": account_activation_token.make_token(user=new_user),
            })

            new_user.email_user(subject , message)
            return render(request , "account/register_done.html" , {"new_user":new_user})
        return render(request , "account/register.html" , {"form":form})
    
class EmailVerification(View):
    def get(self , request , uidb64 , token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        try :
            user = get_object_or_404(User , pk=uid)
        except User.DoesNotExist:
            user = None
        if user and account_activation_token.check_token(user ,token):
            user.is_active =True
            user.save()
            messages.success(request,"Email verified successfuly")
        else:
            messages.error(request,"Email verification Failed :(")
        return redirect("login")
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
        

class UserList(LoginRequiredMixin ,ListView):
    model = User
    template_name = "account/user/list.html"
    queryset = User.objects.filter(is_active=True)
    context_object_name = "users"
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["section"] = "people"
        return context
    def get_template_names(self):
        if self.request.GET.get("users_only"):
            return ["images/image/list_users.html"]
        return [self.template_name]
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:# task, when paginator tries an empty page, listview turns it into a Http404 error, customize the paginator subclass :)
            return HttpResponse("", status=204)

class UserDetail(LoginRequiredMixin, View):
    def get(self, request, username):
        user = get_object_or_404(User, username= username , is_active= True )
        return render(request ,"account/user/detail.html" , {"section":"people" , "user":user})
    
    def post(self, request , username):
        pass