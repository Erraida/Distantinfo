from django.db import models


# Create your models here.
class Discipline(models.Model):
    name = models.CharField('Название дисциплины', max_length=50)

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = 'Дисциплины'

    def __str__(self):
        return self.name


class Lecture(models.Model):
    discipline = models.ForeignKey(Discipline,on_delete=models.PROTECT,null=True)
    title = models.CharField('Название лекции', max_length=150)
    text = models.TextField('Текст лекции')
    date = models.DateField('Дата публикации',auto_now=True)

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'

    def __str__(self):
        return self.title


class Comment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    autor_name = models.CharField('Имя автора', max_length=50)
    comment_text = models.TextField('Текст комментария')
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    def __str__(self):
        return self.comment_text