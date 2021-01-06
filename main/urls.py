from django.urls import path, include
from . import views
app_name = 'main'
urlpatterns = [
    path('', views.index, name='home'),
    path('about-us', views.about, name='about'),
    path('shelude', views.shelude, name='shelude'),
    path('lections', views.lections, name='lections'),
    path('lections/category/<int:discioline_id>/', views.categories, name='Curr_lecture'),
    path('lections/<int:lecture_id>/', views.lections_detail, name='Curr_lecture'),
    path('lections/<int:lecture_id>/comments/', views.comment, name='comment'),
]
