from django.urls import path

from Chat import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('chat/users/list/', views.chat_index, name='chat_user_list'),
    path('chat/users/<int:chat_id>/', views.index, name='index'),
    path('chat/users/register', views.formclass.as_view(), name='register'),
    path('chat/users/login',auth_views.LoginView.as_view(template_name='chat/login.html',),name='login'),
    path('chat/users/logout', views.logout_view, name='logout'),
    path('chat/user/profile/', views.profileListView.as_view(), name='user'),
    path('chat/user/editprofile/', views.profileEdit.as_view(), name='user_edit'),

]