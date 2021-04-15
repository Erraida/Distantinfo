from django.contrib.auth.models import User
from django.template.loader import render_to_string

from main.models import DeferredLecture, DiscList, Discipline, LectRequest
from datetime import datetime


def def_lectire_saveController(request):
    """Сохраняет отложенную лекцю"""
    title = request.POST.get('title')
    full_text = request.POST.get('text')
    dis = request.POST.get('discipline')
    date = request.POST.get('date')
    image = request.POST.get('Image')

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


def lecture_saveController(request,form):
    """Сохраняет лекцю"""
    lection = form.save(commit=False)
    lection.User = request.user
    lection.date = datetime.now()
    lection.save()


def mailController(request):
    """Генерирует массив адресов и рендерит шаблон письма"""
    user_set = User.objects.all()
    text = request.POST.get('text')

    mail_set = []
    for mail in user_set:
        mail_set.append(mail.email)

    mail_set = list(filter(None, mail_set))

    msg_html = render_to_string('editor/lecture_mail.html', {'text': text})

    return mail_set,msg_html


def discipline_ListController(request):
    """Генерирует список дисциплин, доступных пользователю"""
    dis_list = DiscList.objects.filter(username=request.user)
    answers_list = dis_list.values_list('discipline', flat=True)
    return Discipline.objects.filter(id__in=answers_list)


def request_ListController(dis_list):
    """Генерирует список запросов на лекции, доступных пользователю"""
    request_qs = DiscList.objects.none()
    for discipline in dis_list:
        lect_set = LectRequest.objects.filter(
            Discipline=discipline,
            is_done=None
        )
        request_qs = request_qs | lect_set

    return request_qs