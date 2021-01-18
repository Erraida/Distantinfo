from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import UpdateView

from .forms import Registrstion,Login,AccauntForm,RoleRequest,NoteForm
from .models import UserAccount, Notes
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.template.loader import render_to_string


from DistantInform import settings
from django.core.mail import send_mail

# Create your views here.
def register(request):
    if request.method == "POST":
        RegForm = Registrstion(request.POST)
        if RegForm.is_valid():
            RegForm.save()
            mail = request.POST.get('email')
            login = request.POST.get('username')
            usr_id = User.objects.get(username=login).id
            Profile = UserAccount(User_id=usr_id)
            Profile.save()
            msg_html = render_to_string('accounts/email.html', {'login': login})
            send_mail(
                'Подтверждение регистрации',
                'Вы успешнно зарегестрировались на сайте дистанционного информирования',
                settings.EMAIL_HOST_USER,
                [mail],
                html_message=msg_html,
                fail_silently=True

            )
            redirect('accounts:register')
        else:
            messages.error(request,'Ошибка регистрации')
    else:
        RegForm = Registrstion()
    forms = {
        'RegForm':RegForm
    }
    return render(request,'accounts/register.html',{'forms':forms})

def Signup(request):
    if request.method == "POST":
        LogForm = Login(data=request.POST)
        if LogForm.is_valid():
            user = LogForm.get_user()
            login(request,user)
            return redirect('main:home')
        else:
            messages.error(request,'Ошибка регистрации')
    else:
        LogForm = Login()
    forms = {
            'LogForm':LogForm
        }
    return render(request,'accounts/signup.html',{'forms':forms})

def Logout(request):
    logout(request)


def profile(request):
    user = UserAccount.objects.get(User=request.user)
    if request.method == "POST":
        NotForm = NoteForm(request.POST)
        if NotForm.is_valid():
            Note = NotForm.save(commit=False)
            Note.User = request.user
            Note.save()
            return redirect('accounts:account_profile')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        NotForm = NoteForm()
    notes = Notes.objects.filter(User=request.user)
    return render(request,'accounts/profile.html',{'user_account':user,'Noteform':NotForm,'notes':notes})

class UpdateInfo (UpdateView):
    slug_field = 'User'
    slug_url_kwarg = 'user'
    form_class = AccauntForm
    model = UserAccount

    template_name = 'accounts/user_info.html'

def request(request):
    if request.method == "POST":
        ReqForm = RoleRequest(request.POST)
        if ReqForm.is_valid():

            Req = ReqForm.save(commit=False)
            Req.User = request.user
            try:
                Req.save()
                return redirect('accounts:account_profile')
            except:
                messages.error(request,'Ошибка запроса')
    else:
        ReqForm = RoleRequest()

    return render(request,'accounts/request.html',{'RegForm':ReqForm})
