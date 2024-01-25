from django import forms
from .models import Species, Owner


class AddPostForm(forms.Form): # не связанная с моделью
    titile = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False)
    is_published = forms.BooleanField(required=False)
    spec = forms.ModelChoiceField(queryset=Species.objects.all())
    owner = forms.ModelChoiceField(queryset=Owner.objects.all(), required=False)
    
    
