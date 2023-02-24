from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Leaderboard


@login_required
def leaderboard(request):
    leaderboard_data = Leaderboard.objects.order_by('-level', '-quiz_count')
    context = {'globalLeaderboard': leaderboard_data}
    return render(request, 'app/leaderboard.html', context)
