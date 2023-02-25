from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..models import Leaderboard


@login_required
def leaderboard(request):
    leaderboard_data = Leaderboard.objects.order_by('-level', 'quiz_count')
    users = User.objects.all()
    user_data = []
    for user in users:
        user_leaderboard_data = leaderboard_data.filter(user=user).first()
        user_data.append({
            'username': user.username,
            'level': user_leaderboard_data.level if user_leaderboard_data else 1,
            'quiz_count': user_leaderboard_data.quiz_count if user_leaderboard_data else 0
        })
    
    user_data = sorted(user_data, key=lambda x: x['level'], reverse=True)
    context = {
        'globalLeaderboard': leaderboard_data,
        'user_data': user_data
    }

    return render(request, 'app/leaderboard.html', context)