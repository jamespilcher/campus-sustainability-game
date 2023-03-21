from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from app.models import Leaderboard
from ..models import Friend


# add the login required decorator
@login_required
# profile function
def profile(request, username):

    # Get the user object associated with the user logged in
    user = get_object_or_404(User, username=username)

    # Get the leaderboard data sorted by level then xp,
    # and then get the current user's data from that.
    leaderboard_data = Leaderboard.objects.order_by('-level', '-xp')
    current_user_data = Leaderboard.get_current_user_data(
        user, leaderboard_data)

    # Set the context variables
    context = {
        'current_user': user,
        'current_user_data': current_user_data,
        'are_friends': Friend.are_friends(request.user, user),
        'self': Friend.is_self(request.user, user),
        'friends': Friend.get_friends(user),
    }
    # render the profile page
    return render(request, 'accounts/profile.html', context)
