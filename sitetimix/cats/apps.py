from django.apps import AppConfig


class CatsConfig(AppConfig):
    verbose_name = "Котики"
    default_auto_field = "django.db.models.BigAutoField"
    name = "cats"
