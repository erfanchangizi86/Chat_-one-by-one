from django.apps import AppConfig
from django.apps import apps


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Chat'
    verbose_name = "سیستم چت"

    # def ready(self):
    #     PrivetChat = apps.get_model('Chat', 'PrivetChat')
    #     Message = apps.get_model('Chat', 'Message')