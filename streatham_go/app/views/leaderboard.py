from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def leaderboard(request):
    return render(request, 'app/leaderboard.html')
