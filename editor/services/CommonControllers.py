from django.http import HttpResponse
from django.shortcuts import redirect
from xlsxwriter import Workbook

from accounts.models import Group, UserAccount
from editor.forms import SheludeForm
from main.models import Shelude


def students_ListController():
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


    book.close()

    return response

def shelude_saveController(request):
    Shelude_list = Shelude.objects.all()
    if request.method == "POST":
        ShellForm = SheludeForm(request.POST)
        if ShellForm.is_valid():
            ShellForm.save()
            return redirect('main:shelude')
    else:
        ShellForm = SheludeForm()

    return Shelude_list, ShellForm