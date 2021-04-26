from io import StringIO

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import UpdateView

from .services.LectureControllers import *
from .services.CommonControllers import *

from .tasks import *
from .forms import LectureForm, SheludeForm, EventForm
from main.models import Shelude, LectRequest
from accounts.models import Group


def is_lector(user):
    return user.groups.filter(name='Лектор').exists()


def is_shelude(user):
    return user.groups.filter(name='Составитель расписаний').exists()


def save_students_table(request):
    return students_ListController()


@login_required
@user_passes_test(is_lector, login_url='/lections')
def index(request):
    global request_set
    error = ''
    if request.method == "POST":
        form = LectureForm(request.POST)
        is_delayed = request.POST.get('rel_pub')

        if form.is_valid():
            if is_delayed:
                def_lectire_saveController(request)
            else:
                lecture_saveController(request, form)
                mail_set,msg_html = mailController(request)
                sendTask = group(
                    lecture_mail.s(mail_set,msg_html),
                    discord_send.s(
                        request.POST.get('title'),
                        request.POST.get('text')[:100])
                )
                sendTask.apply_async()

            return redirect('editor:editor')

        else:
            error = 'Форма пустая'
    else:
        form = LectureForm()

    dis_list = discipline_ListController(request)
    form.fields['discipline'].queryset = dis_list

    if dis_list.count() == 0:
        error = 'Вам не присвоена ни одна дисциплина'

    lect = Lecture.objects.filter(User=request.user)
    data = {
        'form': form,
        'error': error,
        'lect': lect,
        'requests': request_ListController(dis_list)
    }

    return render(request, 'editor/editor.html', data)


@login_required
@user_passes_test(is_lector, login_url='/lections')
def lectures_list(request):
    lectures_list = Lecture.objects.filter(User=request.user)
    return render(request, 'editor/editor.html', {'lecture': lectures_list})


@login_required
@user_passes_test(is_shelude, login_url='/lections')
def shelude_save(request):
    Shelude_list, ShellForm = shelude_saveController(request)
    return render(request, 'editor/shelude.html', {'Shelude': Shelude_list, 'SheludeForm': ShellForm})

def event_sheldue_save(request):
    if request.method == "POST":
        NewEventForm = EventForm(request.POST)
        NewEventForm.save()
        return redirect('editor:event')
    else:
        NewEventForm = EventForm()
    return render(request, 'editor/shelude.html', {'SheludeForm': NewEventForm})

@login_required
@user_passes_test(is_shelude, login_url='/lections')
def get_shelude_list(request, pk):
    Shelude_list = Shelude.objects.get(id=pk)
    return render(request, 'editor/shelude_view.html', {'shelude': Shelude_list})


@login_required
@user_passes_test(is_shelude, login_url='/lections')
def shelude_del(request, pk):
    Shelude.objects.get(id=pk).delete()
    return redirect('editor:shelude')


@login_required
@user_passes_test(is_lector, login_url='/lections')
def lecture_del(request, pk):
    Lecture.objects.get(id=pk).delete()
    return redirect('editor:editor')


@login_required
@user_passes_test(is_lector, login_url='/lections')
def students_list(request):
    groups = Group.objects.all()
    return render(request, 'editor/students.html', {'groups': groups})


# Представления

class shelude_update(UserPassesTestMixin, UpdateView):
    form_class = SheludeForm
    model = Shelude
    template_name = 'editor/shelude_update.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Составитель расписаний').exists()

    def handle_no_permission(self):
        return redirect('main:home')


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


