from django import template
from django.contrib.auth.models import User

register = template.Library()
from accounts.models import UserAccount,Group

@register.filter()
def Students(things, disc):
    try:
        students = UserAccount.objects.filter(Group=disc)
        return students
    except:
        return 0

@register.filter()
def email(things, user):
    try:
        email = User.objects.get(username=user)
        return email.email
    except:
        return 0