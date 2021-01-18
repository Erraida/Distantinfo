from django.db import models
from accounts.models import Group
from django.contrib.auth.models import User



# Create your models here.
class Discipline(models.Model):
    name = models.CharField('Название дисциплины', max_length=50)

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = 'Дисциплины'

    def __str__(self):
        return self.name


class Lecture(models.Model):
    User = models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    discipline = models.ForeignKey(Discipline,on_delete=models.PROTECT,null=True)
    title = models.CharField('Название лекции', max_length=150)
    text = models.TextField('Текст лекции')
    date = models.DateField('Дата публикации',auto_now=True)

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/editor/'


class Comment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    autor_name = models.CharField('Имя автора', max_length=50)
    comment_text = models.TextField('Текст комментария')
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    def __str__(self):
        return self.comment_text


class Day(models.Model):
    day = models.CharField('День', max_length=15)

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'



class Shelude(models.Model):
    Group = models.ForeignKey(Group,on_delete=models.PROTECT, null=True)
    Day = models.ForeignKey(Day, on_delete=models.PROTECT, null=True)
    first_lect = models.ForeignKey(Discipline,  on_delete=models.PROTECT, related_name= 'first_lect', verbose_name='Первая пара',     blank=True, null=True)
    second_lect = models.ForeignKey(Discipline, on_delete=models.PROTECT, related_name='second_lect', verbose_name='Вторая пара',     blank=True, null=True)
    thrid_lect = models.ForeignKey(Discipline,  on_delete=models.PROTECT, related_name='thrid_lect',  verbose_name='Третья пара',     blank=True, null=True)
    four_lect = models.ForeignKey(Discipline,   on_delete=models.PROTECT, related_name='four_lect',   verbose_name='Четвертая пара',  blank=True, null=True)
    five_lect = models.ForeignKey(Discipline,   on_delete=models.PROTECT, related_name='five_lect',   verbose_name='Пятая пара',      blank=True,null=True)

    def __str__(self):
        return self.Group.group_num

    def get_absolute_url(self):
        return '/editor/shelude/'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        unique_together = ('Group', 'Day')

class Favorite(models.Model):
        User = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
        Lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=False)

        def __str__(self):
            return self.User.username

        class Meta:
            verbose_name = 'Закладка'
            verbose_name_plural = 'Закладки'
            unique_together = ('User', 'Lecture')

class LectRequest(models.Model):
    Discipline = models.ForeignKey(Discipline,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField('Тема',max_length=100)
    is_done = models.BooleanField('Выполнен',null=True)

    def __str__(self):
        return self.title

class DiscList (models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    discipline = models.ForeignKey(Discipline,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.discipline.name

    class Meta:
        verbose_name = 'Список дисциплин'
        verbose_name_plural = 'Списки дисциплин'
        unique_together = ('username', 'discipline')
