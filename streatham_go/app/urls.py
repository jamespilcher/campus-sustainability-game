from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

# set the app name
app_name = 'app'
# create a list of url patterns
urlpatterns = [
    # home page
    path('home/', views.home, name='home'),
    # leaderboard page
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    # ladning page
    path('', views.index, name='index'),
    # play page
    path('play/<token>', views.play, name='play'),
    # conversation javascript (this needs to be rendered)
    path('app/conversion.js', views.conversation, name='conversation'),
    # play javascript (this needs to be rendered)
    path('app/play.js', views.play_js, name='play_js'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# also add the static files to the url patterns
