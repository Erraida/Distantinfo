from django.urls import path, include
from . import views
app_name = 'editor'
urlpatterns = [
    path('', views.index, name='editor'),
    ]