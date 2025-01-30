import os
import django
from django.contrib.auth import get_user_model
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()
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

    def get_last_message_preview(self, length=20):
        """
        Returns a preview of the last message in the chat (up to `length` characters).
        """
        last_message = self.messages.order_by('-timestamp').first()
        if last_message:
            return last_message.content[:length] + ("..." if len(last_message.content) > length else "")
        return "No messages yet."


class Message(models.Model):
    chat = models.ForeignKey('Chat.PrivetChat', on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"
    # def __str__(self):
    #     return f"{self.sender.username}: {self.content[:20]}"

    def chat_message(self):
        return Message.objects.filter(chat=self.chat, sender=self.sender, content=self.content)



class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')

    def __str__(self):
        return self.user.username
