import json

from asgiref.sync import async_to_sync

from .models import PrivetChat,Message
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope['user']
        self.chat = PrivetChat.objects.get(id=self.chat_id)
        if self.user not in [self.chat.user1, self.chat.user2]:
            self.close()

        self.room_group_name = f"chat_{self.chat_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        messages  = Message.objects.create(
            chat=self.chat,
            sender=self.user,
            content=message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.user.username,
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        self.send(text_data=json.dumps({
         "message": message,
        'sender': sender,
        }))