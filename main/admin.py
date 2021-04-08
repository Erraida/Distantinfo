from django.contrib import admin
from .models import Lecture, DeferredLecture, Comment,Discipline,Shelude,Day,Favorite,LectRequest,DiscList
from django.db.models import Count
# Register your models here.
class LectModel(admin.ModelAdmin):
    def comments_count(self, obj):
        return obj.comment_set.count()

    comments_count.short_description = 'Комментарии'
    list_display = ('title', 'discipline','comments_count')

class def_LectModel(admin.ModelAdmin):
    list_display = ('title', 'discipline')

class DisModel(admin.ModelAdmin):
    def dis_count(self, obj):
        return obj.lecture_set.count()

    dis_count.short_description = 'Количество лекций'

    list_display = ('name', 'dis_count')

class ShellDisp(admin.ModelAdmin):
    list_display = ('Group','Day')

class LectReq(admin.ModelAdmin):
    list_display = ('user','Discipline','title','is_done')

class DisListWiew(admin.ModelAdmin):
    list_display = ('discipline', 'username')

admin.site.register(DiscList,DisListWiew)

admin.site.register(Lecture,LectModel)
admin.site.register(DeferredLecture,def_LectModel)
admin.site.register(Comment)
admin.site.register(Discipline,DisModel)
admin.site.register(Shelude,ShellDisp)
admin.site.register(Day)
admin.site.register(Favorite)
admin.site.register(LectRequest,LectReq)

