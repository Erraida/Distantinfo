from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User

from django.shortcuts import redirect
from django.template.loader import render_to_string

from accounts.forms import Registrstion, Login
from accounts.models import UserAccount

from .tasks import *

def registration(request):
    RegForm = Registrstion(request.POST)
    if RegForm.is_valid():
        RegForm.save()
        login = request.POST.get('username')
        usr_id = User.objects.get(username=login).id
        Profile = UserAccount(User_id=usr_id)
        Profile.save()

        mail = request.POST.get('email')
        msg_html = render_to_string('accounts/email.html', {'login': login})

        reg_mail = register_confirm.s(mail, msg_html)
        reg_mail.apply_async()


    else:
        messages.error(request, 'Ошибка регистрации')

