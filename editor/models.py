from django.db import models
from main.models import Discipline
# Create your models here.

class Group(models.Model):
    group_num = models.CharField('Название группы', max_length=10)

    def __str__(self):
        return self.group_num
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

class Shelude(models.Model):
    Discipline = models.ForeignKey(Discipline,on_delete=models.PROTECT,null=True)
    Group = models.ForeignKey(Group,on_delete=models.PROTECT,null=True)
    day = models.IntegerField('День недели')
    lecture = models.IntegerField('Номер пары')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


