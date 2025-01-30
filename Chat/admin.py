# Chat/admin.py
import os

import django
# from django.contrib import admin
# from Chat.models import PrivetChat, Message,profile
#
# @admin.register(PrivetChat)
# class PrivetChatAdmin(admin.ModelAdmin):
#     list_display = ('user1', 'user2',)  # مثال فیلدها
#     # search_fields = ('user1', 'user2')  # جستجو بر اساس کاربران
#
# # اگر نیاز به مدیریت Message نیز دارید، آن را این‌طور ثبت کنید:
# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('chat', 'sender', 'content', 'timestamp')
#
# @admin.register(profile)
# class ProAdmin(admin.ModelAdmin):
#     # list_display = ('user_id')
#     pass