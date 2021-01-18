from django import forms
from django.forms import ModelForm, TextInput, Select


from editor.models import Group
from .models import LectRequest

class seachForm (forms.Form):
    seach = forms.CharField(label='', max_length=100,
                            widget=forms.TextInput(
                            attrs={
                                'placeholder': 'Поиск',
                                'class':'seach'}))

class groupForm (forms.Form):
    group = forms.ModelChoiceField(Group.objects.all(),
                                    label='',
                                    widget=forms.Select(
                                        attrs={
                                            'class':'group',
                                            'name':'group',
                                            'onchange': 'groupForm.submit();'
                                                }))
    def __init__(self, *args, **kwargs):
            super(groupForm, self).__init__(*args, **kwargs)
            self.fields['group'].empty_label = "Выберите группу"



class LectReqForm (ModelForm):
    class Meta:
        model = LectRequest
        fields = ['Discipline', 'title']
        widgets = {
            'Discipline' :Select(attrs={
                'class':'req'
            }),
            'title':TextInput(
                attrs={
                    'class':'req',
                    'placeholder':'Название'
                }
            )
        }

    def __init__(self, *args, **kwargs):
            super(LectReqForm, self).__init__(*args, **kwargs)
            self.fields['Discipline'].empty_label = "Выберите дисциплину"
            self.fields['Discipline'].label = "Дисциплина"