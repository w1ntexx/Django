from django import template
import cats.views as views

register = template.Library()

@register.simple_tag
def get_categories():
    return views.categories_db