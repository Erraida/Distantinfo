from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group as user_group
# Create your models here.

class Group(models.Model):
    group_num = models.CharField('Название группы', max_length=15)

    def __str__(self):
        return self.group_num

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

class UserAccount(models.Model):
    User = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    Group = models.ForeignKey(Group,on_delete=models.PROTECT,null=True,blank=True)
    surname = models.CharField('Фамилия',max_length=50,null=True,blank=True)
    name = models.CharField('Имя', max_length=50,null=True,blank=True)
    mid_name = models.CharField('Отчество', max_length=50,null=True,blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.User.username

    def get_absolute_url(self):
        return '/accounts/profile/'

class RequestRole(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    Group = models.ForeignKey(user_group,on_delete=models.CASCADE,null=False)
    Is_approved = models.BooleanField('Одобрено', null=True)

    class Meta:
        unique_together = ('User', 'Group')
        verbose_name = 'Запрос роли'
        verbose_name_plural = 'Запросы роли'

    def __str__(self):
        return self.User.username

class Notes(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    note = models.TextField('Заметка',max_length=1000)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return self.note