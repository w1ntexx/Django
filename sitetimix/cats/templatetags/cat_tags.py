from django import template
from cats.models import Species, TagPost
from django.db.models import Count

import cats.views as views

# https://docs.djangoproject.com/en/4.2/ref/models/database-functions/

register = template.Library()


# Include Tage используется для определенных шаблонов,
# и регистрация происходит через словарь.
@register.inclusion_tag("cats/list_categories.html")  # путь к templates/apps/template.html
def show_categories(spec_selected=0):
    specs = Species.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {"specs": specs, "spec_selected": spec_selected}

@register.inclusion_tag("cats/list_tags.html")
def show_all_tags():
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)} 
