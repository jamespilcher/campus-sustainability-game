from django.urls import path

from . import views

# set the app name
app_name = 'accounts'
# create a list of url patterns
urlpatterns = [
    # register page
    path('register/', views.register, name='register'),
    # login page
    path('login/', views.login_view, name='login'),
    # logout page
    path('logout/', views.logout_view, name='logout'),
    # search page
    path('search/', views.search, name='search'),
    # profile page
    path('profile/<username>/', views.profile, name='profile'),
    # add friend page
    path('profile/<username>/add', views.add, name='add'),
    # activate user page
    path('<username>/activate/', views.activate, name='activate'),
    # add xp path
    path('<username>/xp', views.xp, name='xp'),
    # add privacy policy path
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
]
