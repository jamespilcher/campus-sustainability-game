from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


# Create your models here.
class Friend(models.Model):
    user1 = models.OneToOneField(User,
                                 on_delete=models.CASCADE,
                                 related_name="user1")
    user2 = models.OneToOneField(User,
                                 on_delete=models.CASCADE,
                                 related_name="user2")

    @classmethod
    def are_friends(self, user1, user2):
        if Friend.objects.filter(user1__in=[user1, user2],
                                 user2__in=[user1, user2]).exists():
            return True
        return False

    @classmethod
    def is_self(self, user1, user2):
        return True if user1 == user2 else False

    @classmethod
    def get_friends(self, user):
        all_friends = Friend.objects.filter(Q(user1=user)
                                            | Q(user2=user)).all()
        friends = []
        for friend in all_friends:
            friends.append(friend.user1 if friend.user2
                           == user else friend.user2)
        return friends
