from django.apps import AppConfig
from django.apps import apps


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Chat'
    verbose_name = "سیستم چت"

    # def ready(self):
    #     from django.contrib.auth import get_user_model
    #     User = get_user_model()