from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models.base import Model as Model
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.core.cache import cache
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    FormView,
)
from .utils import DataMixin
from .models import Cat, TagPost
from .forms import AddPostForm, ContactForm



class CatHome(DataMixin, ListView):
    template_name = "cats/index.html" 
    context_object_name = "posts"  
    title_page = "Главная страница"
    spec_selected = 0
    
    def get_queryset(self):
        w_lst = cache.get('cat_posts')
        if not w_lst:
            w_lst = Cat.published.all().select_related("spec")
            cache.set('cat_posts', w_lst, 60)
        
        return w_lst

@login_required
def about(request):
    contact_list = Cat.published.all()
    paginator = Paginator(contact_list, 3)
    
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "cats/about.html", {"title": "О сайте", "page_obj": page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = "cats/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)

    def get_object(self):
        return get_object_or_404(Cat.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "cats/addpage.html"
    title_page = "Добавления статьи"
    permission_required = "cat.add_cat" # <app>.<action>_<table>
    
    
    def form_valid(self, form):
        cat = form.save(commit=False)
        cat.author = self.request.user
        return super().form_valid(form)
    
    

class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Cat
    fields = "__all__"
    template_name = "cats/addpage.html"
    title_page = "Редактирование статьи статьи"
    permission_required = "cat.change_cat" 


# @permission_required(perm="cat.view_cat", raise_exception=True)
# def contact(request):
#     return render(request, "cats/contact.html", {"title": "Обратная связь"})

class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = "cats/contact.html"
    success_url = reverse_lazy("home")
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class CatSpecies(DataMixin, ListView):
    template_name = "cats/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Cat.published.filter(spec__slug=self.kwargs["spec_slug"]).select_related("spec")

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
