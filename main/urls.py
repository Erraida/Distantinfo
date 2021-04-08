from django.urls import path, include
from . import views
app_name = 'main'
urlpatterns = [
    path('', views.index, name='home'),
    path('about-us', views.about, name='about'),

    path('shelude/', views.shelude_view, name='shelude'),
    path('shelude/<int:group_id>/', views.shelude_view, name='cshelude'),

    path('lections', views.lections, name='lections'),
    path('lections/seach', views.lections, name='seach'),
    path('lections/category/<int:discioline_id>/', views.lections, name='Curr_lecture'),
    path('lections/<int:lecture_id>/', views.lections_detail, name='Curr_lecture'),
    path('lections/<int:lecture_id>/comments/', views.comment, name='comment'),

    path('favorite/<int:lect>/', views.favorite, name='favorite'),
    path('request/', views.makerequest, name='request'),

    path('shelide_jquery/', views.shelude_jquery, name='shelide_jquery'),


]
