from django.db import models
# https://docs.djangoproject.com/en/4.2/ref/models/fields/

class Cat(models.Model):
    title = models.CharField(max_length=255)  # VARCHAR(255)
    content = models.TextField(blank=True)  # TEXT, поле может быть пустым
    time_create = models.DateTimeField(auto_now_add=True)  # НОВАЯ УНИКАЛЬНАЯ запись будет добавлятся автоматически
    time_update = models.DateTimeField(auto_now=True)  # Меняет ТЕКУЩУЮ запись
    is_published = models.BooleanField(default=True)  # is_published = True по дефолту
