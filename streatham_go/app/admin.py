from django.contrib import admin
from app.models import Location, Leaderboard, Game
# Register your models here.

# register all the models to the admin page
admin.site.register(Leaderboard)
admin.site.register(Location)
admin.site.register(Game)
