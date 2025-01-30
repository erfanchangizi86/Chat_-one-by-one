import os

import django
from django.urls import re_path
from Chat.consumers import ChatConsumer

websocket_urlpatterns = [

    re_path(r'ws/chat/(?P<chat_id>\d+)/$',ChatConsumer.as_asgi()),

]
