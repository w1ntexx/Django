from django.db import models
from django.urls import reverse
# https://docs.djangoproject.com/en/4.2/ref/models/fields/

class PublishedManager(models.Manager): # переопределили стандартный менеджер "objects"
    def get_queryset(self): # извлечения данных из бд
        return super().get_queryset().filter(is_published=Cat.Status.PUBLISHED)

class Cat(models.Model):
    
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    # Последовательность полей по умолчанию будет последовательной
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True) 
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)  # НОВАЯ УНИКАЛЬНАЯ запись будет добавлятся автоматически
    time_update = models.DateTimeField(auto_now=True)  # Меняет ТЕКУЩУЮ запись
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    # ManyToOne
    spec = models.ForeignKey("Species", on_delete=models.PROTECT, related_name="posts") 
                                            # "Species" - строка, так как класс определен после текущей модели
                                            # PROTECT - запрещаем удалять связные записи
    
    objects = models.Manager() 
    published = PublishedManager()
    
    
    def __str__(self) -> str:
        return self.title

    # https://docs.djangoproject.com/en/4.2/ref/models/options/
    class Meta:
        ordering = ["-time_create"]
        indexes = [
            models.Index(fields=["-time_create"]),  # Ускоряет поиск по полю, но увеличивает объем данных
        ]
    
    def get_absolute_url(self):
        return reverse('post', kwargs={"post_slug": self.slug}) 
    

class Species(models.Model): # Категория: Породы
    name = models.CharField(max_length=100, db_index=True) 
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("species", kwargs={"spec_slug": self.slug})
    


