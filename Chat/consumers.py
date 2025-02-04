import json
import os

import django
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from redis.cluster import command

from Chat.models import PrivetChat, Message,profile
class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        pass

    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope['user']
        self.chat = PrivetChat.objects.get(id=self.chat_id)

        if self.user not in [self.chat.user1, self.chat.user2]:
            self.close()
            return

        self.room_group_name = f"chat_{self.chat_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
    commands = {
            'new_message': new_message,
        }

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        try:
            message_content = data['message']

            # بررسی صحت داده‌ها قبل از ذخیره
            if not message_content.strip():  # بررسی خالی بودن پیام
                raise ValueError("محتوای پیام نمی‌تواند خالی باشد.")

            message = Message.objects.create(
                chat=self.chat,
                sender=self.user,
                content=message_content
            )

            pro =  profile.objects.filter(user=self.user).first()
            avatar_url = "/media/avatars/default.jpg"  # مقدار پیش‌فرض

            if pro and pro.avatar:
                avatar_url = pro.avatar.url  # دسترسی به URL تصویر

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message.content,
                    "sender": self.user.username,
                    "profile": avatar_url,
                }
            )

            if self.user.username == message.sender.username:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "send_notification",
                        "message": message.content,
                        "sender": self.user.username,
                        "profile": avatar_url,
                    }
                )

        except (KeyError, ValueError) as e:
            print(f"خطا در پردازش پیام: {e}")  # در محیط توسعه برای بررسی مشکل
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")


    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'message',
            "message": event["message"],
            "sender": event["sender"],
            'profile': event["profile"],
        }))

    def send_notification(self, event):
        self.send(text_data=json.dumps({
            'type': 'notification',
            "message": event["message"],
            "sender": event["sender"],
            'profile': event["profile"],
            'chat_id':self.chat_id
        }))
    def send_img(self,event):
        print(event)
        self.send(text_data=json.dumps({}))
