from django.contrib import admin, messages
from django.db.models.functions import Length
from .models import Cat, Species

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ("title", "time_create", "is_published", "spec", "brief_info")
    list_display_links = ("title", )
    # сортировка исключительно для админ панели
    ordering = ["-time_create", "title"] 
    # если мы что-то добавляем в editable должны убрать из links
    list_editable = ("is_published", )
    list_per_page = 10 # пагинация 
    actions = ["set_published", "set_draft"] # действия админки
     
    @admin.display(description="Краткое описание", ordering=Length("content"))
    def brief_info(self, cat: Cat):
        return f"Описание: {len(cat.content)} символов"
    
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