from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Create a leaderboard model containing the user, their level, and their quiz count
class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    quiz_count = models.IntegerField(default=0)
