from django.urls import path, include
from . import views
app_name = 'accounts'
urlpatterns = [
    path('registration/', views.register, name='register'),
    path('login/', views.Signup, name='signup'),
    path('login/', views.Logout, name='Logout'),

    path('update/<str:user>/', views.UpdateInfo.as_view(), name='account_update'),
    path('profile/', views.profile, name='account_profile'),
    path('request/', views.request, name='account_request'),
]