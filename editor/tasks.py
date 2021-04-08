import os
from datetime import datetime

from celery import shared_task, group
from discord_webhook import DiscordWebhook, DiscordEmbed
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

from DistantInform import settings
from main.models import Lecture, DeferredLecture


@shared_task
def lecture_mail(mail_set,msg_html):
    for mail in mail_set:
        print(mail)
        send_mail(
            'Опубликованна новая лекция',
            'Вы успешнно зарегестрировались на сайте дистанционного информирования',
            settings.EMAIL_HOST_USER,
            [mail],
            html_message=msg_html,
            fail_silently=False

        )


@shared_task
def discord_send(em_title, text):
    webhook = DiscordWebhook(
        url='https://discord.com/api/webhooks/796701849948389416/X8f187OlSZSiHdy3idgf5kqeYrmcwkmmZqmKus6_WNGlu5LjeNAVoaBsXSzXhgdb4F4s')
    embed = DiscordEmbed(title=em_title, description=text, color=242424)
    webhook.add_embed(embed)
    response = webhook.execute()


@shared_task
def Lecture_check():
    user_set = User.objects.all()
    DefLect = DeferredLecture.objects.all()

    for lect in DefLect:
        lectTime = lect.date
        CurTime = datetime.today()
        if lectTime < CurTime:
            new_lect = Lecture(
                        title=lect.title,
                        discipline=lect.discipline,
                        text=lect.text,
                        date=lect.date,
                        User=lect.User,
                        image=lect.image
                        )

            new_lect.save()
            lect.delete()

            mail_set = []
            for mail in user_set:
                mail_set.append(mail.email)
            mail_set = list(filter(None, mail_set))

            msg_html = render_to_string('editor/lecture_mail.html', {'text': lect.text})

            sendTask = group(lecture_mail.s(mail_set, msg_html), discord_send.s(lect.title, lect.text))
            sendTask.apply_async()





@shared_task(ignore_result=True)
def add_new():
    g = group(discord_send.s())
    g.apply_async()