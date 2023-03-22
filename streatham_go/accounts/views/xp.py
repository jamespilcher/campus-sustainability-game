from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models import Leaderboard
from django.http import HttpResponse


# calculate the xp for a given quiz count
def _calculate_xp(g):
    # return 100 / (g + 4)
    return 100 / (g + 4)


# user the login_required decorator
@login_required
# add xp to the user
def xp(request, username):
    # get the user
    user = User.objects.get(username=username)
    # get the leaderboard entry
    leaderboardEntry = Leaderboard.objects.get(user=user)
    # calculate the xp
    xp = _calculate_xp(leaderboardEntry.quiz_count)
    # add the xp to the leaderboard entry
    leaderboardEntry.xp += xp
    # increment the quiz count
    leaderboardEntry.quiz_count += 1
    # save the leaderboard entry
    leaderboardEntry.save()
    # return a 200 response
    return HttpResponse()
