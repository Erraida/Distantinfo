from django.urls import path, include
from . import views
app_name = 'editor'
urlpatterns = [
    path('', views.index, name='editor'),
    path('my/', views.lectures_list, name='my'),
    path('<int:pk>/', views.lecture_update.as_view(), name='lecture_up'),
    path('del/<int:pk>/', views.lecture_del, name='lecture_del'),
    path('request/<int:pk>/', views.Requsets_update.as_view(), name='request'),

    path('students/', views.students_list, name='students'),

    path('shelude/', views.shelude_save, name='shelude'),
    path('shelude/<int:pk>/', views.shelude_update.as_view(), name='shelude_up'),
    path('shelude/view/<int:pk>/', views.get_shelude_list, name='shelude_currect'),
    path('shelude/del/<int:pk>/', views.shelude_del, name='shelude_del'),

    path('event/', views.event_sheldue_save, name='event'),

    path('export/', views.save_students_table, name='export'),
    ]