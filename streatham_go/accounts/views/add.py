from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..models import Friend


@login_required
def add(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        r = HttpResponse('')
        r.status_code = 406
        return r

    if Friend.are_friends(request.user, other_user):
        r = HttpResponse('')
        r.status_code = 406
        return r

    f = Friend(user1=request.user, user2=other_user)
    f.save()

    return HttpResponse('')
