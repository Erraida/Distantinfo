from django.forms import ModelForm,TextInput,Textarea,Select

from main.models import Lecture, Discipline
from django import forms


class LectureForm(ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'discipline', 'text']
        widgets = {
            'title' : TextInput(attrs={
                'class': 'lect_edit',
                'placeholder' : 'Название'
            }),
            'discipline':Select(attrs={
                'class':'lect_edit'
            }),
            'text':Textarea(attrs={
                'class':'lect-edit'})
        }
