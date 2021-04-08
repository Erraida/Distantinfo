from io import StringIO

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import UpdateView

from .forms import LectureForm, SheludeForm, DiscList
from main.models import Shelude, Lecture, LectRequest, Discipline, DeferredLecture
from accounts.models import Group, UserAccount

from .tasks import *

from xlsxwriter.workbook import Workbook


def your_view(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=test.xlsx"

    book = Workbook(response, {'in_memory': True})
    bold = book.add_format(
        {'bold': True,
         'bg_color': 'black',
         'font_color': 'white'}
    )
    group = Group.objects.all()

    for group in group:
        user = UserAccount.objects.filter(Group=group).order_by('surname')
        sheet = book.add_worksheet(str(group))
        i = 1
        sheet.write('A1', 'Фамилия', bold)
        sheet.write('B1', 'Имя', bold)
        sheet.write('C1', 'Отчество', bold)
        for user in user:
            i += 1
            print(user.name)
            sheet.write(f'A{i}', str(user.surname))
            sheet.write(f'B{i}', str(user.name))
            sheet.write(f'C{i}', str(user.mid_name or '-'))
        print(' ')

    book.close()

    return response


def is_lector(user):
    return user.groups.filter(name='лох').exists()


def is_shelude(user):
    return user.groups.filter(name='лох').exists()


@login_required
@user_passes_test(is_lector, login_url='/lections')
def index(request):
    global request_set
    error = ''
    if request.method == "POST":
        form = LectureForm(request.POST)
        title = request.POST.get('title')
        full_text = request.POST.get('text')
        dis = request.POST.get('discipline')
        text = full_text[:100]
        pubcheck = request.POST.get('rel_pub')
        date = request.POST.get('date')
        image = request.POST.get('Image')

        if form.is_valid():
            user_set = User.objects.all()
            if pubcheck:
                autor = request.user
                DefLecture = DeferredLecture(
                    title=title,
                    text=full_text,
                    discipline_id=dis,
                    date=date,
                    image=image,
                    User=autor
                )
                DefLecture.save()

            else:
                lection = form.save(commit=False)
                lection.User = request.user
                lection.save()
                mail_set = []
                for mail in user_set:
                    mail_set.append(mail.email)
                mail_set = list(filter(None, mail_set))

                msg_html = render_to_string('editor/lecture_mail.html', {'text': text})

                sendTask = group(lecture_mail.s(mail_set, msg_html), discord_send.s(title, text))
                sendTask.apply_async()

            return redirect('editor:editor')
            # return render(request, 'editor/lecture_mail.html', {'text': text})
        else:
            error = 'Форма пустая'
    else:
        form = LectureForm()
    dis_list = DiscList.objects.filter(username=request.user)

    answers_list = dis_list.values_list('discipline', flat=True)
    form.fields['discipline'].queryset = Discipline.objects.filter(id__in=answers_list)

    none_qs = dis_list.none()
    for discipline in dis_list:
        lect_set = LectRequest.objects.filter(
            Discipline=discipline.discipline,
            is_done=None
        )
        none_qs = none_qs | lect_set

    # Подсчет количества доступных лекций
    amoung = dis_list.count()
    if amoung == 0:
        error = 'Вам не присвоена ни одна дисциплина'

    lect = Lecture.objects.filter(User=request.user)
    data = {
        'form': form,
        'error': error,
        'lect': lect,
        'requests': none_qs
    }

    return render(request, 'editor/editor.html', data)


@login_required
@user_passes_test(is_lector, login_url='/lections')
def lectures_list(request):
    lectures_list = Lecture.objects.filter(User=request.user)
    return render(request, 'editor/editor.html', {'lecture': lectures_list})


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


@login_required
@user_passes_test(is_lector, login_url='/lections')
def students_list(request):
    groups = Group.objects.all()
    return render(request, 'editor/students.html', {'groups': groups})


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
