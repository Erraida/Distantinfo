from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LectureForm



# Create your views here.

def index(request):
    error = ''
    if request.method == "POST":
        form = LectureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('editor:editor')
        else:
            error = 'Форма пустая'


    form = LectureForm()
    data = {
        'form':form,
        'error':error
    }


    return render(request, 'editor/editor.html',data)
