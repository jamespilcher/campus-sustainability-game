from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..models import Leaderboard


def get_current_user_rank(user, user_data, current_user_data):
    return user_data.index(
        {
            'username': user.username,
            'level': current_user_data.level,
            'quiz_count': current_user_data.quiz_count
        }) + 1

def get_current_user_data(user, leaderboard_data):
    return leaderboard_data.filter(user=user).first()


def get_user_data(leaderboard_data):
    user_data = []
    for user_leaderboard_data in leaderboard_data:
        user_data.append({
            'username': user_leaderboard_data.user.username,
            'level': user_leaderboard_data.level,
            'quiz_count': user_leaderboard_data.quiz_count
        })
    return user_data

@login_required
def leaderboard(request):
    leaderboard_data = Leaderboard.objects.order_by('-level', 'quiz_count')
    
    user_data = get_user_data(leaderboard_data)
    user_data = sorted(user_data, key=lambda x: x['level'], reverse=True)

    # Find the current user's leaderboard data and rank
    current_user_data = get_current_user_data(request.user, leaderboard_data)
    current_user_rank = get_current_user_rank(request.user, user_data, current_user_data)

    context = {
        'globalLeaderboard': leaderboard_data,
        'user_data': user_data,
        'current_user_data': current_user_data,
        'current_user_rank': current_user_rank
    }

    return render(request, 'app/leaderboard.html', context)
