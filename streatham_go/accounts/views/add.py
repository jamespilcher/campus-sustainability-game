from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..models import Friend


@login_required
def add(request, username):
    # get the user from the database
    other_user = get_object_or_404(User, username=username)
    # check if the user is the current user
    if other_user == request.user:
        # if the user is the current user, return a 406
        r = HttpResponse('')
        r.status_code = 406
        return r

    # check if the user is already a friend
    if Friend.are_friends(request.user, other_user):
        # if the user is already a friend, return a 406
        r = HttpResponse('')
        r.status_code = 406
        return r

    # create a friend object
    f = Friend(user1=request.user, user2=other_user)
    f.save()

    # return a 200
    return HttpResponse('')
