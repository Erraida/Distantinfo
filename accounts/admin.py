from django.contrib import admin
from .models import UserAccount,Group,RequestRole,Notes
# Register your models here.

class UserAcc(admin.ModelAdmin):
    list_display = ('User','surname', 'name','mid_name','Group')

class Request(admin.ModelAdmin):
    list_display = ('User','Group','Is_approved')

class Note(admin.ModelAdmin):
    list_display = ('User','note')

admin.site.register(UserAccount,UserAcc)
admin.site.register(Group)
admin.site.register(RequestRole,Request)
admin.site.register(Notes,Note)
