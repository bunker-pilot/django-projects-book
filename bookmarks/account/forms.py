from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# question about the get_user_model() , if we were going to use the User model then why bother with this piece of useless gorbage
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

"""
class UserRegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput , label="Password")
    repeat_password = forms.CharField(widget=forms.PasswordInput , label="Repeat password")

    class Meta:
        model = User
        fields = ["username" , "email" , "first_name"]

    def clean_password(self):
        cd  =self.cleaned_data
        for i in cd.keys():
            print(i)
        if cd["password"] != cd.get("repeat_password"):
            raise forms.ValidationError("Passwords don't match!")
        return cd["repeat_password"]
    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email = cd["email"]).exists():
            raise forms.ValidationError("A user with this emaol already exists!")
        return cd["email"]
"""
class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField( required=True , max_length = 300)
    class Meta:
        model = get_user_model()
        fields = ["username" , "email" , "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email
class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name" , "last_name" , "email"]

    def clean_email(self):
        cd = self.cleaned_data["email"]

        qs = User.objects.filter(email= cd).exclude(id = self.instance.id)
        if qs.exists():
            raise forms.ValidationError("This email has already been used")
        return cd

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo" , "date_of_birth"]

