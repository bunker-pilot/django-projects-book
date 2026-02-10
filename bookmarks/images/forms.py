from django import forms 
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from .models import Image

class ImageForm(forms.ModelForm):   
    class Meta:
        model = Image
        fields = ["title" , "url" , "description"]
        widgets = {
            "url" : forms.HiddenInput(),
        }
    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = ["jpeg" , "jpg" , "png"]
        extension = url.rsplit("." , 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("This image format is not supported!")
        return url 
    def save(self,commit =True):
        image = super().save(commit = False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit("." , 1)[1].lower()
        image_name = f"{name}.{extension}"
        response = requests.get(image_url)
        response.raise_for_status()
        image.image.save(
            image_name, ContentFile(response.content), save = False
        )
        if commit:
            image.save()
        return image