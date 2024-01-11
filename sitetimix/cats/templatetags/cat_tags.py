from django import template
import cats.views as views

register = template.Library()

# Simple tag используется как обычный тег {% tag %}
# и регистрируется как обычный шаблон.
@register.simple_tag(name="getcats")
def get_categories():
    return views.categories_db

# Include Tage используется для определенных шаблонов,
# и регистрация происходит через словарь.
@register.inclusion_tag("cats/list_categories.html")  # путь к templates/apps/template.html
def show_categories(cat_selected=0):
    cats = views.categories_db
    return {'cats': cats, 'cat_selected': cat_selected}

# Здесь cat_selected, это значение в функции представления, где он равен cat_id
# Соответсвенно, каждый раз, когда мы нажимаем на одну из категории, cat_selected равен id этой категории
# Теперь в шаблнах мы пишем условие, что если cat_selected пустой
# То "Все категории" подсвечиваются, а иначе, подсвечивается только то, что будет cat_id
# Значит, если я нажму на одну из категорий, она подсветится, а "Все категории" нет.
