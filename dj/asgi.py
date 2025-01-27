import os
import django  # اضافه کردن این خط
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import Chat.routing

# تنظیمات Django را بارگذاری می‌کنیم
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocha.settings')
django.setup()  # این خط را اضافه کنید

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(Chat.routing.websocket_urlpatterns)
    ),
})
