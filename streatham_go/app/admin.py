from django.contrib import admin
from app.models import Location, Question, Leaderboard, Game
# Register your models here.

# register all the models to the admin page
admin.site.register(Location)
admin.site.register(Question)
admin.site.register(Leaderboard)
admin.site.register(Game)
