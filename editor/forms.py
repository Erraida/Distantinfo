import datetime

from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm, TextInput, Textarea, Select, HiddenInput, DateTimeField, DateTimeInput

from main.models import Lecture, Shelude, SessionShelude
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

class EventForm (ModelForm):
    date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'lect_edit',
            'placeholder': 'Дата проведения',
            'autocomplete':'off'


        }))
    comment_text = forms.Textarea(attrs={
        'id': 'comment',
        'placeholder': 'Название'
    })
    class Meta:
        model = SessionShelude
        fields = '__all__'

        widgets = {
            'Group': Select(attrs={
                'class': 'lect_edit'
            }),
            'Discipline': Select(attrs={
                'class': 'lect_edit'
            }),
            'Type': Select(attrs={
                'class': 'lect_edit'
            }),
            'Building': Select(attrs={
                'class': 'lect_edit'
            }),
            'Room': TextInput(attrs={
                'class': 'lect_edit',
                'placeholder': 'Аудитория'
            }),

        }
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['Group'].empty_label = "Выберите группу"
        self.fields['Group'].label = ""
        self.fields['Building'].empty_label = "Выберите здание"
        self.fields['Building'].label = ""
        self.fields['Type'].empty_label = "Выберите тип"
        self.fields['Type'].label = ""
        self.fields['Discipline'].empty_label = "Выберите предмет"
        self.fields['Discipline'].label = ""
        self.fields['date'].label = ""
        self.fields['Room'].label = ""
