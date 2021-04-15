import datetime

from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm, TextInput, Textarea, Select, HiddenInput, DateTimeField, DateTimeInput

from main.models import Lecture,Shelude
from main.models import DiscList
from django import forms


class LectureForm(ModelForm):
    text = forms.CharField(widget=CKEditorWidget())
    date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        required=False,
        widget=forms.DateTimeInput(attrs={
             'class': 'lect_edit',
              'placeholder' : 'Дата публикации',
              'disabled':'true'

        }))


    class Meta:
        model = Lecture
        fields = ['discipline','title', 'date','rel_pub','text']
        widgets = {
           'title' : TextInput(attrs={
                'class': 'lect_edit',
                'placeholder' : 'Название'
            }),
            'discipline':Select(attrs={
                'class':'lect_edit'
            }),


        }
    def __init__(self, *args, **kwargs):
        super(LectureForm, self).__init__(*args, **kwargs)
        self.fields['discipline'].empty_label = "Выберите дисциплину"
        self.fields['discipline'].label = ""
        self.fields['text'].label = ""
        self.fields['title'].label = ""
        self.fields['date'].label = ""
        self.fields['rel_pub'].label = "Отложенная публикация"


class SheludeForm(ModelForm):
    class Meta:
        model = Shelude
        fields = '__all__'