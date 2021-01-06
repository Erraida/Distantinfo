from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from  django.core.paginator import Paginator
from .models import Lecture, Comment, Discipline


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def shelude(request):
    return render(request, 'main/shelide.html')


def lections(request):
    Lectures = Lecture.objects.all()
    Disciplines = Discipline.objects.all()

    paginator = Paginator(Lectures,2)
    page_num = request.GET.get('page',1)
    page_objects = paginator.get_page(page_num)

    return render(request, 'main/lectures.html', {'Lectures': Lectures, 'Disciplines': Disciplines,'page_obj':page_objects})


def categories(request,discioline_id):
    Disciplines = Discipline.objects.all()
    Lectures = Lecture.objects.all().filter(discipline = discioline_id)
    Discipline_name = Discipline.objects.get(id=discioline_id)

    paginator = Paginator(Lectures, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    return render(request, 'main/lectures.html', {'Lectures': Lectures, 'Disciplines': Disciplines,'Descipline_id': discioline_id,'page_obj':page_objects, 'Discipline_name':Discipline_name})


def lections_detail(request, lecture_id):
    try:
        lect = Lecture.objects.get(id=lecture_id)
    except:
        raise Http404('Статья не найдена')
    return render(request, 'main/currect_lecturies.html', {'lecture': lect})


def comment(request, lecture_id):
    try:
        lect = Lecture.objects.get(id=lecture_id)
    except:
        raise Http404('Статья не найдена')
    if request.method == 'GET':
        name = request.GET['name']
        text = request.GET['textf']
    lect.comment_set.create(autor_name=name, comment_text=text)
    return HttpResponseRedirect(reverse('main:Curr_lecture', args=(lect.id,)))
