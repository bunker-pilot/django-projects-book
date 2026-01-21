from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Profile

# question about the get_user_model() , if we were going to use the User model then why bother with this piece of useless gorbage
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
    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email = cd["email"]).exists():
            raise forms.ValidationError("A user with this emaol already exists!")
        return cd["email"]
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

