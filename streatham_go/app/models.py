from django.contrib.auth.models import User
from django.db import models


# Games Model
class Game(models.Model):
    # The name of the game
    name = models.CharField(max_length=50)
    # The file name of the game
    file = models.CharField(max_length=50)


# Questions Model
class Question(models.Model):
    question = models.CharField(max_length=200)
    a = models.CharField(max_length=200)
    b = models.CharField(max_length=200)
    c = models.CharField(max_length=200)
    d = models.CharField(max_length=200)
    answer = models.CharField(max_length=1)


# Location model
class Location(models.Model):
    # the name of the building
    name = models.CharField(max_length=50)
    # the longitude of the building
    latitude = models.CharField(max_length=50)
    # the latitude of the building
    longitude = models.CharField(max_length=50)
    # a message given by the building
    message = models.CharField(max_length=200)
    # the icon of the building
    icon = models.ImageField(upload_to='app/icons/', blank=True, null=True)
    # The name of the game that is played at the building
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


# The leaderboard model
class Leaderboard(models.Model):
    # One to one relationship with the User model
    # When a user is deleted, their leaderboard entry is deleted
    # User has a level, xp value, and quiz_count
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    quiz_count = models.IntegerField(default=0)

    # Gets the rank of the user within the leaderboard
    @classmethod
    def get_current_user_rank(self, user, user_data, current_user_data):
        return user_data.index(
            {
                'username': user.username,
                'level': current_user_data.level,
                'xp': current_user_data.xp,
                'quiz_count': current_user_data.quiz_count
            }) + 1

    # Gets the leaderboard data for the current user
    @classmethod
    def get_current_user_data(self, user, leaderboard_data):
        return leaderboard_data.filter(user=user).first()

    # Gets the leaderboard data for all users
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
