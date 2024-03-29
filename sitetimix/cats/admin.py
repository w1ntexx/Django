from typing import Any
from django.contrib import admin, messages
from django.db.models.functions import Length
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from .models import Cat, Species

class OwnerFilter(admin.SimpleListFilter):
    title = "Статус владения"
    parameter_name = "status"
    
    def lookups(self, request, model_admin):
        return [
            ("owned", "Принадлежит"),
            ("unowned", "Не принадлежит")
        ]
    
    def queryset(self, request, queryset):
        if self.value() == "owned":
            return queryset.filter(owner__isnull=False)
        if self.value() == "unowned":
            return queryset.filter(owner__isnull=True)
    
@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    fields = ["title", "content", "photo", "post_photo", "slug", "spec", "owner", "tags"] # поля для редактирования
    # exclude - иключает поля для редактирования
    readonly_fields = ["post_photo"] 
    prepopulated_fields = {"slug": ("title", )} # автозаполнение
    list_display = ("title", "post_photo", "time_create", "is_published", "spec")
    list_display_links = ("title",)
    # сортировка исключительно для админ панели
    ordering = ["-time_create", "title"] 
    # если мы что-то добавляем в editable должны убрать из links
    list_editable = ("is_published", )
    list_per_page = 10 # пагинация 
    actions = ["set_published", "set_draft"] # действия админки
    search_fields = ["title__icontains", "spec__name"] # через __ можно писать люкапы
    list_filter = [OwnerFilter, "spec__name", "is_published"] 
    save_on_top = True
    
     
    @admin.display(description="Изображение", ordering="content")
    def post_photo(self, cat: Cat):
        if cat.photo:
            return mark_safe(f"<img src={cat.photo.url} alt={cat.title} width=50>")
        return "Без фото"
    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Cat.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записей")

    @admin.action(description="Снять с публикации")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Cat.Status.DRAFT)
        self.message_user(request, f"Снято {count} записей", messages.WARNING)


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    


    