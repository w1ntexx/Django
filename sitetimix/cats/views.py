from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    Http404,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify, first

desc = """  Абиссинская порода — это элегантные кошки средних размеров с сильными грациозными телами и длинными стройными лапами. Для этой породы характерны округлая клиновидная форма головы с большими миндалевидными глазами и уши с небольшими кисточками на кончиках. Короткая прилегающая шерсть абиссинской кошки отличается тикингом — смешением цветов на каждом из волосков. Наиболее популярный окрас — «дикий» (ruddy), но также встречаются и другие виды.</p>>
"""

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]

# data_db  Имитация в учебных целях базы данных, с которой мы работаем в шаблоне
data_db = [
    {"id": 1, "title": "Абиссинская кошка", "content": desc, "is_published": True},
    {"id": 2,"title": "Австралийский мист","content": "Описание Австралийского миста",
        "is_published": True,},
    {"id": 3, "title": "Сноу-шу", "content": "Описание Сноу-шу", "is_published": True},
]


categories_db = [
    {"id": 1, "name": "Породы"},
    {"id": 2, "name": "Питомники кошек"},
    {"id": 3, "name": "Основные этапы жизни кошек"},
]


# Главная страница, которая рендрит шаблон index.html
def index(request):
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": data_db,
        "cat_selected": 0,
    }
    return render(request, "cats/index.html", data)


def about(request):
    data = {
        "title": "О сайте",
        "menu": menu,
    }
    return render(request, "cats/about.html", context=data)


def show_post(request, post_id):
    return HttpResponse(f"Отоброжение статьи с id = {post_id}")


def add_page(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, cat_id):
    data = {
        "title": "Отображение по рубрикам",
        "menu": menu,
        "posts": data_db,
        "cat_selected": cat_id,
    }
    return render(request, "cats/index.html", context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")
