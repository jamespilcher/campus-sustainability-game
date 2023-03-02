from django.contrib import admin
from app.models import Location, Question, Leaderboard
# Register your models here.

admin.site.register(Location)
admin.site.register(Question)
admin.site.register(Leaderboard)
