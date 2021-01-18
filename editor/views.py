from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import UpdateView

from DistantInform import settings

from .forms import LectureForm, SheludeForm, DiscList
from main.models import Shelude, Lecture, LectRequest,Discipline

from discord_webhook import DiscordWebhook, DiscordEmbed
from django.core.mail import send_mail
from DistantInform import settings


def discord_send(em_title, text):
    webhook = DiscordWebhook(
        url='https://discord.com/api/webhooks/796701849948389416/X8f187OlSZSiHdy3idgf5kqeYrmcwkmmZqmKus6_WNGlu5LjeNAVoaBsXSzXhgdb4F4s')
    embed = DiscordEmbed(title=em_title, description=text, color=242424)
    webhook.add_embed(embed)
    response = webhook.execute()


def is_lector(user):
    return user.groups.filter(name='лох').exists()


def is_shelude(user):
    return user.groups.filter(name='лох').exists()


# Create your views here.
@login_required
@user_passes_test(is_lector, login_url='/lections')
def index(request):
    global request_set
    error = ''
    if request.method == "POST":
        form = LectureForm(request.POST)
        title = request.POST.get('title')
        text = request.POST.get('text')
        dis = request.POST.get('discipline')
        text = text[:100]
        print(text)
        print(title)
        print(dis)

        if form.is_valid():
            user_set = User.objects.all()
            lection = form.save(commit=False)
            lection.User = request.user
            lection.save()
            mail_set = []
            for mail in user_set:
                mail_set.append(mail.email)
            mail_set = list(filter(None, mail_set))
            print(mail_set)
            discord_send(title, text)
            for i in mail_set:
                send_mail(
                    'Подтверждение регистрации',
                    text,
                    settings.EMAIL_HOST_USER,
                    [i],
                    fail_silently=False
                )
            return redirect('editor:editor')
        else:
            error = 'Форма пустая'
    else:
        form = LectureForm()
    dis_list = DiscList.objects.filter(username=request.user)

    answers_list = dis_list.values_list('discipline', flat=True)
    print(answers_list)
    form.fields['discipline'].queryset = Discipline.objects.filter(id__in=answers_list)
    # работа со списком доступных лекций



    none_qs = dis_list.none()
    for discipline in dis_list:
        lect_set = LectRequest.objects.filter(Discipline=discipline.discipline,is_done=None)
        none_qs = none_qs|lect_set

    for id in none_qs:
        print(id.id)
    # Подсчет количества доступных лекций
    amoung = dis_list.count()
    if amoung == 0:
        error = 'Вам не присвоена ни одна дисциплина'

    lect = Lecture.objects.filter(User=request.user)
    data = {
        'form': form,
        'error': error,
        'lect': lect,
        'requests':none_qs
    }

    return render(request, 'editor/editor.html', data)
@login_required
@user_passes_test(is_lector, login_url='/lections')
def lectures_list(request):
    lectures_list = Lecture.objects.filter(User=request.user)
    return render(request, 'editor/editor.html',{'lecture':lectures_list})

@login_required
@user_passes_test(is_lector, login_url='/lections')
def shelude(request):
    Shelude_list = Shelude.objects.all()
    if request.method == "POST":
        ShellForm = SheludeForm(request.POST)
        if ShellForm.is_valid():
            ShellForm.save()
            return redirect('main:shelude')
    else:
        ShellForm = SheludeForm()
    return render(request, 'editor/shelude.html', {'Shelude': Shelude_list, 'SheludeForm': ShellForm})


@login_required
@user_passes_test(is_lector, login_url='/lections')
def shelude_view(request, pk):
    Shelude_list = Shelude.objects.get(id=pk)
    return render(request, 'editor/shelude_view.html', {'shelude': Shelude_list})


@login_required
@user_passes_test(is_lector, login_url='/lections')
def shelude_del(request, pk):
    Shelude.objects.get(id=pk).delete()
    return redirect('editor:shelude')


class shelude_update(UserPassesTestMixin, UpdateView):
    form_class = SheludeForm
    model = Shelude
    template_name = 'editor/shelude_update.html'

    def test_func(self):
        return self.request.user.groups.filter(name='лох').exists()

    def handle_no_permission(self):
        return redirect('main:home')


@login_required
@user_passes_test(is_lector, login_url='/lections')
def lecture_del(request, pk):
    Lecture.objects.get(id=pk).delete()
    return redirect('editor:editor')


class lecture_update(UserPassesTestMixin, UpdateView):
    form_class = LectureForm
    model = Lecture
    template_name = 'editor/shelude_update.html'

    def test_func(self):
        return self.request.user.groups.filter(name='лох').exists()

    def handle_no_permission(self):
        return redirect('main:home')


class Requsets_update(UserPassesTestMixin, UpdateView):
    fields = ['is_done']
    model = LectRequest
    template_name = 'editor/shelude_update.html'

    def test_func(self):
        return self.request.user.groups.filter(name='лох').exists()

    def handle_no_permission(self):
        return redirect('main:home')
