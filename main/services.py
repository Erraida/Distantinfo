from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect

from accounts.models import Group, UserAccount
from main.forms import seachForm, LectReqForm
from main.models import Day, Shelude, Lecture, Discipline, Favorite
from accounts.models import Group




def sheludeService(group_id):
    
    try:
        pon_id = Day.objects.get(day='Понедельник').id
    except:
        pon_id = 1
    try:
        vt_id = Day.objects.get(day='Вторник').id
    except:
        vt_id = 2
    try:
        sr_id = Day.objects.get(day='Среда').id
    except:
        sr_id = 3
    try:
        ch_id = Day.objects.get(day='Четверг').id
    except:
        ch_id = 4
    try:
        pt_id = Day.objects.get(day='Пятница').id
    except:
        pt_id = 5

    try:
        data = Shelude.objects.filter(Group=group_id)
        group = Group.objects.get(id=group_id)

        pn = data.filter(Day=pon_id)
        vt = data.filter(Day=vt_id)
        sr = data.filter(Day=sr_id)
        ch = data.filter(Day=ch_id)
        pt = data.filter(Day=pt_id)

        days = (pn,vt,sr,ch,pt)
    except:
        pn=None
        vt=None
        sr=None
        ch=None
        pt=None
        days = (pn,vt,sr,ch,pt)

    return days,group

def lectionsService(request, *args, **kwargs):
    discioline_id = None

    if 'discioline_id' in kwargs:
        discioline_id = kwargs.get('discioline_id')
        Lectures = Lecture.objects.all().filter(discipline=discioline_id)

    elif 'seach' in kwargs:
        seach = kwargs.get('seach')
        Lectures = Lecture.objects.all().filter(title__icontains=seach)
    else:
        Lectures = Lecture.objects.all()

    Disciplines = Discipline.objects.all()

    paginator = Paginator(Lectures, 5)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    Seach = seachForm()

    return Seach,Lectures,Disciplines,discioline_id,page_objects,page_num


def lection_detail(lecture_id):
    try:
        lect = Lecture.objects.get(id=lecture_id)
    except:
        raise Http404('Статья не найдена')

    user = lect.User
    autor = UserAccount.objects.get(User=user)

    return lect,autor


def add_to_fav (request,lect):
    try:
        FavEl = Favorite(User=request.user, Lecture_id=lect)
        FavEl.save()
    except:
        pass

def makerequest (request):
    Request = LectReqForm(request.POST)

    if Request.is_valid():
        Request_obj = Request.save(commit=False)
        Request_obj.user = request.user
        Request_obj.save()
        return redirect('main:lections')
