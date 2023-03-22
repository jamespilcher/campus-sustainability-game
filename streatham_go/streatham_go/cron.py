# cron.py

from app.models import Leaderboard

def reset_times_played_today():
    # Leaderboard.objects.update(timesPlayedToday=0)
    # Update every leaderboard object to set timesPlayedToday to 0
    print("Times played today reset")
    Leaderboard.objects.all().update(timesPlayedToday=0)
