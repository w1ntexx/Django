from django import template
import cats.views as views
from cats.models import Species

register = template.Library()


# Include Tage используется для определенных шаблонов,
# и регистрация происходит через словарь.
@register.inclusion_tag("cats/list_categories.html")  # путь к templates/apps/template.html
def show_categories(spec_selected=0):
    specs = Species.objects.all()
    return {'specs': specs, 'spec_selected': spec_selected}

# Здесь spec_selected, это значение в функции представления, где он равен spec_id
# Соответсвенно, каждый раз, когда мы нажимаем на одну из категории, spec_selected равен id этой категории
# Теперь в шаблнах мы пишем условие, что если spec_selected пустой
# То "Все категории" подсвечиваются, а иначе, подсвечивается только то, что будет spec_id
# Значит, если я нажму на одну из категорий, она подсветится, а "Все категории" нет.
