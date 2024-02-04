from django.db.models.base import Model as Model
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .utils import DataMixin
from .models import Cat, TagPost, UploadFile
from .forms import AddPostForm, UploadFileForm
from django.core.files.storage import default_storage
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)



class CatHome(DataMixin, ListView):
    template_name = "cats/index.html" 
    context_object_name = "posts"  
    title_page = "Главная страница"
    spec_selected = 0
    
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
        request, "cats/about.html", {"title": "О сайте", "form": form}
    )


class ShowPost(DataMixin, DetailView):
    template_name = "cats/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, select=1, title=context["post"].title)

    def get_object(self):
        return get_object_or_404(Cat.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "cats/addpage.html"
    title_page = "Добавления статьи"
    
    
class UpdatePage(DataMixin, UpdateView):
    model = Cat
    fields = "__all__"
    template_name = "cats/addpage.html"
    title_page = "Редактирование статьи статьи"


def contact(request):
    return render(request, "cats/contact.html")


def login(request):
    return HttpResponse("Авторизация")


class CatSpecies(DataMixin, ListView):
    template_name = "cats/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Cat.published.filter(
            spec__slug=self.kwargs["spec_slug"]).select_related("spec")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spec = context["posts"][0].spec
        return self.get_mixin_context(
            context=context,
            title=f"Категория - {spec.name}",
            spec_selected=spec.pk,
        )

class TagPostList(DataMixin, ListView):
    template_name = "cats/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(
            context=context,
            title=f"Тег - {tag.tag}",
        )

    def get_queryset(self):
        return Cat.published.filter(tags__slug=self.kwargs["tag_slug"])
