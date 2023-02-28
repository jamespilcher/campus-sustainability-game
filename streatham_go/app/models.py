from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50)
    distance = models.IntegerField()
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    def __str__(self):
        return self.location
    

# Create your models here.


class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    quiz_count = models.IntegerField(default=0)

    @classmethod
    def get_current_user_rank(self, user, user_data, current_user_data):
        return user_data.index(
            {
                'username': user.username,
                'level': current_user_data.level,
                'xp': current_user_data.xp,
                'quiz_count': current_user_data.quiz_count
            }) + 1

    @classmethod
    def get_current_user_data(self, user, leaderboard_data):
        return leaderboard_data.filter(user=user).first()

    @classmethod
    def get_user_data(self, leaderboard_data):
        user_data = []
        for user_leaderboard_data in leaderboard_data:
            user_data.append({
                'username': user_leaderboard_data.user.username,
                'level': user_leaderboard_data.level,
                'xp': user_leaderboard_data.xp,
                'quiz_count': user_leaderboard_data.quiz_count
            })
        return user_data
