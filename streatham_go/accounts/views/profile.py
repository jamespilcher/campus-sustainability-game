from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from app.models import Leaderboard


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)

    leaderboard_data = Leaderboard.objects.order_by('-level', '-xp')
    current_user_data = Leaderboard.get_current_user_data(
        user, leaderboard_data)
    context = {
        'current_user': user,
        'current_user_data': current_user_data,
    }
    return render(request, 'accounts/profile.html', context)
