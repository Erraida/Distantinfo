from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserAccount,RequestRole,Notes

from DistantInform import settings


class Registrstion(UserCreationForm):
    username = forms.CharField(label='',widget=forms.TextInput(
                            attrs={
                                'placeholder': 'Логин',
                                'class':'logon_form'
                                    }))
    email = forms.CharField(label='',widget=forms.EmailInput(
                            attrs={
                                'placeholder': 'Почта',
                                'class': 'logon_form'
                                    }))
    password1 = forms.CharField(label='',widget=forms.PasswordInput(
                            attrs={
                                'placeholder': 'Пароль',
                                'class':'logon_form'
                                    }))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(
                            attrs={
                                'placeholder': 'Повторите пароль',
                                'class':'logon_form'
                                    }))

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})

class Login(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Имя',
            'class': 'logon_form'
        }))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Пароль',
            'class': 'logon_form'
        }))



class AccauntForm (ModelForm):
    class Meta:
        model = UserAccount
        fields = ['Group','surname','name','mid_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Group'].empty_label = "Выберите группу"
        self.fields['Group'].widget.attrs.update({'class': 'req'})
        self.fields['surname'].widget.attrs.update({'class': 'req','placeholder':'Отчество'})
        self.fields['name'].widget.attrs.update({'class': 'req','placeholder':'Отчество'})
        self.fields['mid_name'].widget.attrs.update({'class': 'req','placeholder':'Отчество'})


class RoleRequest (ModelForm):
    class Meta:
        model = RequestRole
        fields = ['Group']


class NoteForm (ModelForm):
    class Meta:
        model = Notes
        fields = ['note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note'].widget.attrs.update({'class': 'noteform'})