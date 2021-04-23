from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from DistantInform import settings

from .models import Lecture,   Comment
from .forms import groupForm, LectReqForm, CommentForm, seachForm

from .services import sheludeService, lectionsService, lection_detail, add_to_fav
from accounts.models import Group


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def error_404(request, exception):
    render(request, '404.html')


def shelude_jquery(request):
    group_id = 1
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

    days, group,events = sheludeService(group_id)

    data = render_to_string("main/shelide_jquery.html",
                            {
                                'data': days,
                                'group': group,
                                'events': events,

                            })
    return HttpResponse(data)


def shelude_view(request):
    group = groupForm()
    forms = {'group': group}
    return render(request, 'main/shelide.html', {'forms': forms})


def lections(request, *args, **kwargs):
    if request.method == "POST":
        Seach = seachForm(request.POST)
        if Seach.is_valid():
            seach_q = request.POST.get('seach')
            data = lectionsService(request, seach=seach_q)
    else:
        if 'discioline_id' in kwargs:
            data = lectionsService(request, discioline_id=kwargs.get('discioline_id'))
        else:
            data = lectionsService(request)

    Seach, Lectures, Disciplines, discioline_id, page_objects, page_num = data

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
    lect,autor = lection_detail(lecture_id)
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


def add_to_favorite(request, lect):
    add_to_fav(request,lect)
    return HttpResponseRedirect(reverse('main:Curr_lecture', args=(lect,)))


def makerequest(request):
    if request.method == "POST":
        makerequest(request)
    else:
        Request = LectReqForm()

    return render(request, 'main/reqests.html', {'request': Request})


