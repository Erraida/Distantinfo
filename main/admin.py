from django.contrib import admin
from .models import Lecture, Comment,Discipline
# Register your models here.
admin.site.register(Lecture)
admin.site.register(Comment)
admin.site.register(Discipline)