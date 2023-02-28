from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Leaderboard


@login_required
def leaderboard(request):
    leaderboard_data = Leaderboard.objects.order_by('-level', 'quiz_count')
    user_data = Leaderboard.get_user_data(leaderboard_data)
    user_data = sorted(user_data, key=lambda x: x['level'], reverse=True)

    # Find the current user's leaderboard data and rank
    current_user_data = Leaderboard.get_current_user_data(
        request.user, leaderboard_data)
    current_user_rank = Leaderboard.get_current_user_rank(
        request.user, user_data, current_user_data)

    context = {
        'globalLeaderboard': leaderboard_data,
        'user_data': user_data,
        'current_user_data': current_user_data,
        'current_user_rank': current_user_rank
    }

    return render(request, 'app/leaderboard.html', context)
