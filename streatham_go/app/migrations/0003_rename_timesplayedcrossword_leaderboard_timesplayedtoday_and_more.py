# Generated by Django 4.1.6 on 2023-03-22 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_rename_quiz_count_leaderboard_numgamesplayed_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="leaderboard",
            old_name="timesPlayedCrossword",
            new_name="timesPlayedToday",
        ),
        migrations.RemoveField(
            model_name="leaderboard",
            name="timesPlayedHangman",
        ),
        migrations.RemoveField(
            model_name="leaderboard",
            name="timesPlayedTicTacToe",
        ),
        migrations.RemoveField(
            model_name="leaderboard",
            name="timesPlayedTrivia",
        ),
        migrations.RemoveField(
            model_name="leaderboard",
            name="timesPlayedWordSearch",
        ),
    ]
