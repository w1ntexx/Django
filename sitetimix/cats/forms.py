from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Species, Owner


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = "russian"
    
    def __init__(self, message=None):
        self.message = message if message else "Должны присутсвовать только русские символы, дефис и пробел."
        
    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form): 
    title = forms.CharField(max_length=255,
                            min_length=5,
                            label="Заголовок",
                            widget=forms.TextInput(attrs={"class": "form-input"}),
                            error_messages={
                                 "min_length": "Слишком короткий заголовок",
                                 "required": "Без заголовка никак",
                             })
    slug = forms.SlugField(max_length=255,
                           label="URL",
                           validators=[
                                MinLengthValidator(5, message="Минимум 5 символов"),
                                MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    content = forms.CharField(
        widget=forms.Textarea(attrs={"cols": 50, "rows": 5}),
        required=False,
        label="Описание"
        )
    is_published = forms.BooleanField(
        required=False,
        initial=True,
        label="Статус"
        )
    spec = forms.ModelChoiceField(
        queryset=Species.objects.all(),
        empty_label="Порода не выбрана",
        label="Породы"
        )
    owner = forms.ModelChoiceField(
        queryset=Owner.objects.all(),
        required=False,
        empty_label="Нет хозина",
        label="Хозяин"
        )
    
    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "

        if not (set(title) <= set(ALLOWED_CHARS)):
   
            raise ValidationError("Должны присутствовать только русские символы, дефис и пробел.")
        
