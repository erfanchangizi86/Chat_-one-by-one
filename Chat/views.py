from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from Chat.forms import RegisterForm, Test_form
from Chat.models import PrivetChat, Message


@login_required(login_url='/login/')
def chat_index(request):
    ids =  request.user.id
    chats = PrivetChat.objects.filter(Q(user1_id=ids) | Q(user2_id=ids))
    if request.method == 'GET':
        search = request.GET.get('search')
        if search:
            chats = chats.filter(Q(user1__username__icontains=search) | Q(user2__username__icontains=search))
    return render(request,'chat/chat_list.html',{'chats':chats})

# Create your views here.
@login_required(login_url='/login/')
def index(request,chat_id):
    chat = get_object_or_404(PrivetChat, id=chat_id)
    if request.user not in [chat.user1, chat.user2]:
        return HttpResponseForbidden("You do not have access to this chat.")
    messages = chat.messages.all().order_by('timestamp')
    return render(request, 'chat/room.html', {'chat': chat, 'messages': messages,'user': request.user})


class formclass(FormView):
    form_class = Test_form
    template_name = 'chat/register.html'
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        # ذخیره کاربر
        form.save()
        return super().form_valid(form)