from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    Http404,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify, first
from cats.models import Cat, Species, TagPost


menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


# Главная страница, которая рендрит шаблон index.html
def index(request):
    posts = Cat.published.all().order_by("title").select_related("spec")

    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
        "spec_selected": 0,
    }
    return render(request, "cats/index.html", data)


def about(request):
    data = {
        "title": "О сайте",
        "menu": menu,
    }
    return render(request, "cats/about.html", context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Cat, slug=post_slug)

    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "spec_selected": 1,
    }

    return render(request, "cats/post.html", data)


def add_page(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_species(request, spec_slug):
    species = get_object_or_404(Species, slug=spec_slug)
    posts = Cat.published.filter(spec_id=species.pk).select_related("spec")

    data = {
        "title": "Отображение по рубрикам",
        "menu": menu,
        "posts": posts,
        "spec_selected": species.id,
    }
    return render(request, "cats/index.html", context=data)


def show_tagpost(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Cat.Status.PUBLISHED)
    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None,  # когда выбран тег, ни одна из категорий не должна быть выделена
    }

    return render(request, "cats/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")
