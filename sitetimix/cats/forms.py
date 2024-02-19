from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Cat, Species, Owner


class AddPostForm(forms.ModelForm): 
    spec = forms.ModelChoiceField(
        queryset=Species.objects.all(),
        empty_label="Порода не выбрана",
        label="Породы"
        )
    owner = forms.ModelChoiceField(
        queryset=Owner.objects.all(),
        required=False,
        empty_label="Нет хозяина",
        label="Хозяин"
        )
    
    class Meta:
        model = Cat
        fields = [
            "title",
            "slug",
            "content",
            "photo",
            "is_published",
            "spec",
            "tags",
            "owner",
            ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5}),
            
        }
        labels = {"slug": "URL"}

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        
        return title    


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.CharField(label="E-mail")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Описание")    
    captcha = CaptchaField(error_messages={'invalid': 'Неверный CAPTCHA'})
    