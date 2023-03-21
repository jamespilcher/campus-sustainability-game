from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


# friend model
class Friend(models.Model):
    # the user who sent the friend request
    user1 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="user1")
    # the user who received the friend request
    user2 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="user2")

    # check if two users are friends
    @classmethod
    def are_friends(self, user1, user2):
        # check if friend relation exisits
        if Friend.objects.filter(user1__in=[user1, user2],
                                 user2__in=[user1, user2]).exists():
            # if it exists, they are friend
            return True
        # if it doesn't exist, they are not friends
        return False

    # check if two users are the same
    @classmethod
    def is_self(self, user1, user2):
        # check if the users are the same
        return True if user1 == user2 else False

    @classmethod
    # get all friends of a user
    def get_friends(self, user):
        # get all friend relations
        all_friends = Friend.objects.filter(Q(user1=user)
                                            | Q(user2=user)).all()
        # initlaize the list of friends
        friends = []
        # loop through all friend relations
        for friend in all_friends:
            # append the friend that is not the user
            friends.append(friend.user1 if friend.user2
                           == user else friend.user2)
        # return the list of friends
        return friends
