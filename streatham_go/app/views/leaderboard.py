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
    
    # Find the current user's leaderboard data and rank
    current_user_data = leaderboard_data.filter(user=request.user).first()
    current_user_rank = user_data.index({
        'username': request.user.username,
        'level': current_user_data.level if current_user_data else 1,
        'quiz_count': current_user_data.quiz_count if current_user_data else 0
    }) + 1
    
    context = {
        'globalLeaderboard': leaderboard_data,
        'user_data': user_data,
        'current_user_data': current_user_data,
        'current_user_rank': current_user_rank
    }

    return render(request, 'app/leaderboard.html', context)
