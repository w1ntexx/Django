from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
import transliterate

# https://docs.djangoproject.com/en/4.2/ref/models/fields/
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/

class PublishedManager(models.Manager): 
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Cat.Status.PUBLISHED)

class Cat(models.Model):
    
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    # Последовательность полей по умолчанию будет последовательной
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        )
    slug = models.SlugField(
        max_length=100, 
        unique=True,
        db_index=True,
        verbose_name="Slug",
        blank=True
        ) 
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d",
        default=None,
        blank=True,
        null=True,
        verbose_name="Фото")
    content = models.TextField(
        blank=True,
        verbose_name="Текст статьи",
        )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
        )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Время изменения",
        )  
    is_published = models.IntegerField(
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name="Статус",
        )
    spec = models.ForeignKey(
        "Species",
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="Породы",
        ) 
    tags = models.ManyToManyField(
        "TagPost",
        blank=True,
        related_name="tags",
        verbose_name="Теги",
        )                              
    owner = models.OneToOneField(
        "Owner",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Хозяин",
        )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="author"
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliterate.slugify(self.title)
            super().save(*args, **kwargs)
    
    objects = models.Manager() 
    published = PublishedManager()
    
    
    def __str__(self) -> str:
        return self.title
    
    # https://docs.djangoproject.com/en/4.2/ref/models/options/
    class Meta:
        verbose_name = "Котик"
        verbose_name_plural = "Котики"
        
        ordering = ["title", ]
        indexes = [
            models.Index(fields=["title"]),  # Ускоряет поиск по полю, но увеличивает объем данных
        ] # неявный порядок сортировки
    
    def get_absolute_url(self):
        return reverse('post', kwargs={"post_slug": self.slug}) 
    

class Species(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Породы"
        ) 
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True
        )
    
    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("species", kwargs={"spec_slug": self.slug})
    


class TagPost(models.Model):
    tag = models.CharField(
        max_length=100,
        db_index=True,
        )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        )
    
    
    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})


class Owner(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name

class UploadFile(models.Model):
    file = models.FileField(upload_to="uploads_model")