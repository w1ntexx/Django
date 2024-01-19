from django import template
import cats.views as views
from cats.models import Species, TagPost

register = template.Library()


# Include Tage используется для определенных шаблонов,
# и регистрация происходит через словарь.
@register.inclusion_tag("cats/list_categories.html")  # путь к templates/apps/template.html
def show_categories(spec_selected=0):
    specs = Species.objects.all()
    return {"specs": specs, "spec_selected": spec_selected}

@register.inclusion_tag("cats/list_tags.html")
def show_all_tags():
    return {"tags": TagPost.objects.all()} 
    