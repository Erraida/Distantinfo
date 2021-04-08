import json

from django.contrib.auth.models import User
from django.core import serializers
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Lecture, Discipline, DiscList, Comment, Day
from .forms import seachForm, groupForm, LectReqForm, CommentForm
from .models import Shelude, Favorite
from .controllers import sheludeController, lectionsController
from accounts.models import Group, UserAccount


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def error_404(request, exception):
    render(request, '404.html')


def shelude_jquery(request):
    if request.method == "POST":
        group = groupForm(request.POST)

        if group.is_valid():
            group_id = request.POST.get('group')
        else:
            try:
                grp = Group.objects.first()
                group_id = grp.id
            except:
                group_id = 1

    days = sheludeController(group_id)
    data = render_to_string("main/shelide_jquery.html",
                            {
                                'pon': days['pn'],
                                'vt': days['vt'],
                                'sr': days['sr'],
                                'chet': days['ch'],
                                'pt': days['pt'],
                                'group': days['group']

                            })
    return HttpResponse(data)  # Отправка данных


def shelude_view(request):
    group = groupForm()

    forms = {
        'group': group
    }

    return render(request, 'main/shelide.html',
                  {
                      'forms': forms}
                  )


def lections(request, *args, **kwargs):
    if 'discioline_id' in kwargs:

        discioline_id = kwargs.get('discioline_id')
        data = lectionsController(request,discioline_id=discioline_id)

    else:
        data = lectionsController(request)


    Seach, Lectures, Disciplines, discioline_id, page_objects, page_num = data

    print(page_num)
    return render(request, 'main/lectures.html',
                  {
                      'Seach': Seach,
                      'Lectures': Lectures,
                      'Disciplines': Disciplines,
                      'Descipline_id': discioline_id,
                      'page_obj': page_objects,
                      'currect_page': int(page_num),
                  })






def lections_detail(request, lecture_id):
    try:
        lect = Lecture.objects.get(id=lecture_id)
    except:
        raise Http404('Статья не найдена')

    user = lect.User
    autor = UserAccount.objects.get(User=user)
    comment = CommentForm()
    return render(request, 'main/currect_lecturies.html',
                  {
                      'lecture': lect,
                      'autor': autor,
                      'comment': comment
                  })


def comment(request, lecture_id):
    try:
        lect = Lecture.objects.get(id=lecture_id)
    except:
        raise Http404()
    if request.method == 'GET':
        text = request.GET['comment_text']

        comm = Comment(autor_name=request.user, lecture_id=lecture_id, comment_text=text)
        comm.save()

    return HttpResponseRedirect(reverse('main:Curr_lecture', args=(lect.id,)))


def favorite(request, lect):
    try:
        FavEl = Favorite(User=request.user, Lecture_id=lect)
        FavEl.save()
    except:
        pass

    return HttpResponseRedirect(reverse('main:Curr_lecture', args=(lect,)))


def makerequest(request):
    if request.method == "POST":
        Request = LectReqForm(request.POST)

        if Request.is_valid():
            Request_obj = Request.save(commit=False)
            Request_obj.user = request.user
            Request_obj.save()
            return redirect('main:lections')
    else:
        Request = LectReqForm()

    return render(request, 'main/reqests.html', {'request': Request})
