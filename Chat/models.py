import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
# Create your models here.
class PrivetChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')

    def __str__(self):
        return f'{self.user1.username} - {self.user2.username}'
    class Meta:
        verbose_name = "چت خصوصی"
        verbose_name_plural = "چت‌های خصوصی"


class Message(models.Model):
    chat = models.ForeignKey(PrivetChat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"
    # def __str__(self):
    #     return f"{self.sender.username}: {self.content[:20]}"

    def chat_message(self):
        return Message.objects.filter(chat=self.chat, sender=self.sender, content=self.content)