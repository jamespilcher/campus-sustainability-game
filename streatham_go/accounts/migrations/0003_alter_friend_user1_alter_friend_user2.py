# Generated by Django 4.1.6 on 2023-03-01 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0002_friend_delete_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="friend",
            name="user1",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user1",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="friend",
            name="user2",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user2",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
