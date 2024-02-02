from django.db.models.query import QuerySet
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    Http404,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify, first
from .models import Cat, Species, TagPost, UploadFile
from .forms import AddPostForm, UploadFileForm
from django.core.files.storage import default_storage
from django.views import View
from django.views.generic import TemplateView, ListView




menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


# def index(request):
#     posts = Cat.published.all().order_by("title").select_related("spec")

#     data = {
#         "title": "Главная страница",
#         "menu": menu,
#         "posts": posts,
#         "spec_selected": 0,
#     }
#     return render(request, "cats/index.html", data)


class CatHome(ListView):
    model = Cat 
    template_name = "cats/index.html" # стандартный путь предпологает _list.html, мы его переопределяем
    context_object_name = "posts" # стандартное имя object_list, мы его переопределяем для перебора в html-документе
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
        
    return render(request, "cats/about.html",
                  {"title": "О сайте", "menu": menu, "form": form })


def show_post(request, post_slug):
    post = get_object_or_404(Cat, slug=post_slug)

    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "spec_selected": 1,
    }

    return render(request, "cats/post.html", data)


# def add_page(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("home")

#     else:
#         form = AddPostForm()
    
#     data = {
#        "menu": menu,
#        "title": "Добавления статьи",
#        "form": form,
#        }
#     return render(request, "cats/addpage.html", data)


class AddPage(View):
    def data(self, form=None):
        data = {
       "menu": menu,
       "title": "Добавления статьи",
       "form": form,
       }
        return data
    
    def get(self, request):
        data = self.data(AddPostForm())
        return render(request, "cats/addpage.html", data)
    
    def post(self, request):
        data = self.data(AddPostForm(request.POST, request.FILES))
        return render(request, "cats/addpage.html", data)


def contact(request):
    return render(request, "cats/contact.html", {"menu": menu})


def login(request):
    return HttpResponse("Авторизация")


# def show_species(request, spec_slug):
#     species = get_object_or_404(Species, slug=spec_slug)
#     posts = Cat.published.filter(spec_id=species.pk).select_related("spec")

#     data = {
#         "title": "Отображение по рубрикам",
#         "menu": menu,
#         "posts": posts,
#         "spec_selected": species.id,
#     }
#     return render(request, "cats/index.html", context=data)


class CatSpecies(ListView):
    template_name = "cats/index.html"
    context_object_name = "posts"
    allow_empty = False
    
    def get_queryset(self):
        return Cat.published.filter(spec__slug=self.kwargs["spec_slug"]).select_related("spec")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spec = context["posts"][0].spec
        context["title"] = f"Категория - {spec.name}"
        context["menu"] = menu
        context["spec_selected"] = spec.id
        return context
    
    
# def show_tagpost(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Cat.Status.PUBLISHED)
#     data = {
#         "title": f"Тег: {tag.tag}",
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": None,
#     }

#     return render(request, "cats/index.html", context=data)


class CatTag(ListView):
    template_name = "cats/index.html"
    context_object_name = "posts"
    allow_empty = False
    
    def get_queryset(self):
        return Cat.published.filter(tags__slug=self.kwargs["tag_slug"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = context["posts"][0].tags.all()[0]
        context["title"] = f"Тег - {tag.tag}"  
        context["menu"] = menu
        context["cat_selected"] = None
        return context
   