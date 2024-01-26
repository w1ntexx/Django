from django import forms
from .models import Species, Owner


class AddPostForm(forms.Form): # не связанная с моделью
    titile = forms.CharField(max_length=255, label="Заголовок", widget=forms.TimeInput(attrs={"class": "form-input"}))
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 50, "rows": 5}), required=False, label="Контет")
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")
    spec = forms.ModelChoiceField(queryset=Species.objects.all(), empty_label="Порода не выбрана", label="Породы")
    owner = forms.ModelChoiceField(queryset=Owner.objects.all(), required=False, empty_label="Нет хозина", label="Хозяин")
    
    