from django import template
from django.contrib.auth.models import User

from main.models import Lecture, DiscList
from accounts.models import UserAccount

register = template.Library()


@register.filter()
def lecture_coll(things, disc):
    try:
        amoung = Lecture.objects.filter(discipline=disc).count()
        return amoung
    except:
        return 0


@register.filter()
def lector(things, disc):
    try:
        lector_set = DiscList.objects.filter(discipline=disc)
        array = ''
        for lector_set in lector_set:
            user = lector_set.username

            lector_id = User.objects.get(username=user).id
            lector_q = UserAccount.objects.get(User_id=lector_id)
            if lector_q:
                name = lector_q.name
                surname = lector_q.surname
                full_name = str(name) + ' ' + str(surname)

                array = array + full_name + '\r\n'

        return array
    except:
        return None


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        return user.groups.filter(name=group_name).exists()
    except:
        return False
