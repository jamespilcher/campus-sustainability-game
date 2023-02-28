from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Leaderboard


@login_required
def profile(request):
    leaderboard_data = Leaderboard.objects.order_by('-level', '-xp')
    current_user_data = Leaderboard.get_current_user_data(
        request.user, leaderboard_data)
    context = {
        'current_user_data': current_user_data,
    }
    return render(request, 'accounts/profile.html', context)
