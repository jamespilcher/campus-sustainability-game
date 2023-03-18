from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'app'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('', views.index, name='index'),
    path('tictactoe/', views.tictactoe, name='tictactoe'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
