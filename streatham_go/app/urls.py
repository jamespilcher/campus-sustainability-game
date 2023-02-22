from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('', views.index, name='index'),
]
