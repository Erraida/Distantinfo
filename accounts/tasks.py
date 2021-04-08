from celery import shared_task
from django.core.mail import send_mail

from DistantInform import settings

@shared_task
def register_confirm(mail,msg_html):
    print(mail)
    send_mail(
        'Подтверждение регистрации',
        'Вы успешнно зарегестрировались на сайте дистанционного информирования',
        settings.EMAIL_HOST_USER,
        [mail],
        html_message=msg_html,
        fail_silently=False

    )