from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from  django.core.paginator import Paginator

from .models import Lecture, Discipline,DiscList
from .forms import seachForm,groupForm,LectReqForm
from .models import Shelude,Favorite
from accounts.models import Group,UserAccount





# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def shelude(request):
    grp = Group.objects.first()
    group_id = grp.id
    if request.method == "POST":
        group = groupForm(request.POST)

        if group.is_valid():
            group_id = request.POST.get('group')
            print(group)

    group = groupForm()

    forms = {
        'group':group
    }
    group = Group.objects.get(id=group_id)

    pn = Shelude.objects.filter(Group=group_id, Day=1)
    vt = Shelude.objects.filter(Group=group_id, Day=2)
    sr = Shelude.objects.filter(Group=group_id, Day=3)
    ch = Shelude.objects.filter(Group=group_id, Day=4)
    pt = Shelude.objects.filter(Group=group_id, Day=5)
    return render(request, 'main/shelide.html',{'pon':pn,'vt':vt,'sr':sr,'chet':ch,'pt':pt, 'forms':forms,'group':group,})


def lections(request):
    Lectures = Lecture.objects.all()
    Disciplines = Discipline.objects.all()


    paginator = Paginator(Lectures,2)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)

    Seach = seachForm()
    forms = {
        'Seach': Seach,

    }

    return render(request, 'main/lectures.html', {'Lectures': Lectures, 'Disciplines': Disciplines,'page_obj':page_objects,'forms':forms})


def categories(request,discioline_id):
    Disciplines = Discipline.objects.all()
    Lectures = Lecture.objects.all().filter(discipline = discioline_id)
    Discipline_name = Discipline.objects.get(id=discioline_id)

    paginator = Paginator(Lectures, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    Seach = seachForm()
    forms = {
        'Seach': Seach,

    }

    return render(request, 'main/lectures.html', {'Lectures': Lectures, 'Disciplines': Disciplines,'Descipline_id': discioline_id,'page_obj':page_objects, 'Discipline_name':Discipline_name,'forms':forms})


def seach(request):
    Lectures = Lecture.objects.all()
    Disciplines = Discipline.objects.all()
    error = ''
    lectures = ''
    seach_q = '2'
    if request.method == "POST":
        Seach = seachForm(request.POST)

        if Seach.is_valid():
            seach_q = request.POST.get('seach')
            print(seach_q)

            #Добавить нормальный поиск и пагинацию
            Lectures = Lecture.objects.filter(title__icontains=seach_q)
    paginator = Paginator(Lectures, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)


    Seach = seachForm()
    forms = {
        'Seach': Seach,

    }
    return render(request,'main/lectures.html',{ 'forms':forms,'Seach_q': seach_q, 'letc':lectures,'Seach':Seach,'page_obj':page_objects})


def lections_detail(request, lecture_id):
    try:
        lect = Lecture.objects.get(id=lecture_id)
    except:
        raise Http404('Статья не найдена')

    user = lect.User
    autor = UserAccount.objects.get(User=user)
    return render(request, 'main/currect_lecturies.html', {'lecture': lect,'autor':autor})


def comment(request, lecture_id):
    try:
        lect = Lecture.objects.get(id=lecture_id)
    except:
        raise Http404()
    if request.method == 'GET':
        name = request.GET['name']
        text = request.GET['textf']
    lect.comment_set.create(autor_name=name, comment_text=text)
    return HttpResponseRedirect(reverse('main:Curr_lecture', args=(lect.id,)))

def favorite (request,lect):

    try:
        FavEl = Favorite(User=request.user, Lecture_id=lect)
        FavEl.save()
    except:
        return HttpResponseRedirect(reverse('main:Curr_lecture', args=(lect,)))
    return HttpResponseRedirect(reverse('main:Curr_lecture', args=(lect,)))

def makerequest (request):
    if request.method == "POST":
        Request = LectReqForm(request.POST)

        if Request.is_valid():
            Request_obj = Request.save(commit=False)
            Request_obj.user = request.user
            Request_obj.save()
            return redirect('main:lections')
    else:
        Request = LectReqForm()

    return render(request,'main/reqests.html',{'request':Request})


def error_404 (request,exception):
    render(request, '404.html')


