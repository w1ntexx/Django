from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name="Фотография",
        )
    date_birth = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата Рождения",
        )