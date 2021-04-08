from django.core.paginator import Paginator

from accounts.models import Group
from main.forms import seachForm
from main.models import Day, Shelude, Lecture, Discipline
from accounts.models import Group


def sheludeController(group_id):
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

        days = {'pn': pn, 'vt': vt, 'sr': sr, 'ch': ch, 'pt': pt, 'group': group}
    except:

        days = {'pn': None, 'vt': None, 'sr': None, 'ch': None, 'pt': None, 'group': None}

    return days


def lectionsController(request, *args, **kwargs):
    discioline_id = None

    if request.method == "POST":
        Seach = seachForm(request.POST)

        if Seach.is_valid():
            seach_q = request.POST.get('seach')
            Lectures = Lecture.objects.filter(title__icontains=seach_q)
    else:

        if 'discioline_id' in kwargs:
            print(kwargs)
            discioline_id = kwargs.get('discioline_id')
            Lectures = Lecture.objects.all().filter(discipline=discioline_id)

        else:
            Lectures = Lecture.objects.all()

    Disciplines = Discipline.objects.all()

    paginator = Paginator(Lectures, 10)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    Seach = seachForm()

    return Seach,Lectures,Disciplines,discioline_id,page_objects,page_num
