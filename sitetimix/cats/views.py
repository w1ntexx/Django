from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify, first

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]

data_db = [
    {'id': 1, 'title': "Абиссинская кошка", 'content': "Описание Абиссинской кошки", 'is_published': True},
    {'id': 2, 'title': "Австралийский мист", 'content': "Описание Австралийского миста", 'is_published': False},
    {'id': 3, 'title': "Сноу-шу", 'content': "Описание Сноу-шу", 'is_published': True},
]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
    }
    return render(request, "cats/index.html", data)


def about(request):
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, "cats/about.html", context=data)\

def show_post(request, post_id):
    return HttpResponse(f"Отоброжение статьи с id = {post_id}")


def add_page(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")
