from django.apps import AppConfig
from django.utils import timezone
from schedule import Scheduler
from models import reset_times_played_today


class YourAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        scheduler = Scheduler()
        scheduler.timezone = timezone.get_current_timezone()
        scheduler.every().day.at('00:00').do(reset_times_played_today)
        scheduler.start()
