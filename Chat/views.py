from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from Chat.models import PrivetChat


# Create your views here.
@login_required(login_url='/login/')
def index(request,chat_id):
    chat = get_object_or_404(PrivetChat, id=chat_id)
    if request.user not in [chat.user1, chat.user2]:
        return HttpResponseForbidden("You do not have access to this chat.")
    messages = chat.messages.all().order_by('timestamp')
    return render(request, 'chat/room.html', {'chat': chat, 'messages': messages,'user': request.user})