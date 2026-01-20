from django import forms 
from django.contrib.auth import get_user_model
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput , label="Password")
    password2= forms.CharField(widget=forms.PasswordInput , label="Password Repeat")

    class Meta:
        model = get_user_model()
        fields = ["username" , "email" , "first_name"]

    def clean_password(self):
        cd  =self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match!")
        return cd["password2"]
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name" , "last_name" , "email"]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo" , "date_of_birth"]

