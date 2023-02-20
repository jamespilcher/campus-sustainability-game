from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
]
