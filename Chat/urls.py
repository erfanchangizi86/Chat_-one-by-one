from django.urls import path

from Chat import views

urlpatterns = [
    path('chat/users/<int:chat_id>/', views.index, name='index'),
]