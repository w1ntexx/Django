from django import template
from cats.models import Species, TagPost
from django.db.models import Count
from cats.utils import menu 
    
    
register = template.Library()

@register.simple_tag
def get_menu():
    return menu

@register.inclusion_tag("cats/list_categories.html")  
def show_categories(spec_selected=0):
    specs = Species.objects.annotate(total=Count("posts")).filter(posts__is_published=True).filter(total__gt=0)
    return {"specs": specs, "spec_selected": spec_selected}

@register.inclusion_tag("cats/list_tags.html")
def show_all_tags():
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)} 

@register.simple_tag
def get_photo():
    pass
