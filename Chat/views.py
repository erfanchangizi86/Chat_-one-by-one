from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, ListView,UpdateView

from Chat.forms import RegisterForm, Test_form,edit_profile_form
from Chat.models import PrivetChat, Message, profile

User = get_user_model()

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
def index(request, chat_id):
    chat = get_object_or_404(PrivetChat, id=chat_id)

    # بررسی اینکه کاربر در این چت خصوصی عضو است
    if request.user not in [chat.user1, chat.user2]:
        return HttpResponseForbidden("You do not have access to this chat.")

    # دریافت تمام پیام‌های این چت
    messages = chat.messages.all().order_by('timestamp')

    return render(request, 'chat/room.html', {
        'chat': chat,
        'messages': messages,
        'user': request.user,
        'chat_id': chat_id,
    })

class formclass(FormView):
    form_class = Test_form
    template_name = 'chat/register.html'
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        # ذخیره کاربر
        form.save()
        return super().form_valid(form)

 # daphne -p 8005 dj.asgi:application

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


class profileListView(ListView):
    model = User
    template_name = 'chat/profile.html'
    context_object_name = 'user'
    def get_queryset(self):
        query =  super().get_queryset()
        query = query.get(id=self.request.user.id)
        return query


class profileEdit(LoginRequiredMixin,UpdateView):
    model = User
    form_class = edit_profile_form
    template_name = 'chat/edit_profile.html'
    success_url = reverse_lazy('user')

    def get_object(self, queryset=None):
        return self.request.user


class profileEditeImage(LoginRequiredMixin,UpdateView):
    model = profile
    form_class = edit_profile_form
    success_url = reverse_lazy('user')

    def get_object(self, queryset=None):
        return self.request.user.profile