from django.core.management.base import BaseCommand
# Import reset_times_played_today function from cron.py
from app.models import Leaderboard

def reset_times_played_today():
    # Leaderboard.objects.update(timesPlayedToday=0)
    # Update every leaderboard object to set timesPlayedToday to 0
    print("Times played today reset")
    Leaderboard.objects.all().update(timesPlayedToday=0, numGamesPlayed=0)


class Command(BaseCommand):
    help = "Resets the timesPlayedToday field on all leaderboard objects"

    def handle(self, *args, **options):
        reset_times_played_today()
        self.stdout.write(self.style.SUCCESS("Times played today reset"))

