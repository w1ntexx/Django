from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    Http404,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify, first
from django.urls import reverse, reverse_lazy
from .models import Cat, Species, TagPost, UploadFile
from .forms import AddPostForm, UploadFileForm
from django.core.files.storage import default_storage
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
)


menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class CatHome(ListView):
    model = Cat
    template_name = "cats/index.html"  # стандартный путь предпологает _list.html, мы его переопределяем
    context_object_name = "posts"  # стандартное имя object_list, мы его переопределяем для перебора в html-документе
    extra_context = {
        "title": "Главная страница",
        "menu": menu,
        "spec_selected": 0,
    }

    def get_queryset(self):
        return Cat.published.all().order_by("title").select_related("spec")


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFile(file=form.cleaned_data["file"])
            fp.save()
    else:
        form = UploadFileForm()

    return render(
        request, "cats/about.html", {"title": "О сайте", "menu": menu, "form": form}
    )


class ShowPost(DetailView):
    # model = Cat
    template_name = "cats/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["post"].title
        context["menu"] = menu
        context["spec_selected"] = 1

        return context

    def get_object(self):
        return get_object_or_404(Cat.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(FormView):
    form_class = AddPostForm
    template_name = "cats/addpage.html"
    succes_url = reverse_lazy("home")
    extra_context = {
        "title": "Добавления статьи",
        "menu": menu,
    }

    def form_valid(self, form):
        # метод вызывается, как только форма прошла проверку
        form.save()
        return super().form_valid(form)

class UpdatePage(UpdateView):
    model = Cat
    fields = "__all__"
    template_name = "cats/addpage.html"
    extra_context = {
        "title": "Обновление статьи",
        "menu": menu
    }

def contact(request):
    return render(request, "cats/contact.html", {"menu": menu})


def login(request):
    return HttpResponse("Авторизация")


class CatSpecies(ListView):
    template_name = "cats/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Cat.published.filter(spec__slug=self.kwargs["spec_slug"]).select_related(
            "spec"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spec = context["posts"][0].spec
        context["title"] = f"Категория - {spec.name}"
        context["menu"] = menu
        context["spec_selected"] = spec.id
        return context


class TagPostList(ListView):
    template_name = "cats/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        context["title"] = f"Тег - {tag.tag}"
        context["menu"] = menu
        context["cat_selected"] = None
        return context

    def get_queryset(self):
        return Cat.published.filter(tags__slug=self.kwargs["tag_slug"])
