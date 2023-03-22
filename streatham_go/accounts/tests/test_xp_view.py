import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Leaderboard
from django.test import TestCase
from urllib.parse import urlencode


pytest.USER_PASSWORD = '12345'
pytest.USER_WRONG_PASSWORD = 'wrong_password'


@pytest.fixture
def user() -> User:
    u = User.objects.create_user('ethanhofton',
                                 'eh736@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'Ethan'
    u.last_name = 'Hofton'
    u.save()

    lb_entry = Leaderboard()
    lb_entry.user = u
    lb_entry.save()

    return u


@pytest.mark.django_db
def test_xp_view_add_xp(user, client):
    client.login(username=user.username, password=pytest.USER_PASSWORD)
    url = reverse('accounts:xp', args=[user.username])

    leaderboard_entry = Leaderboard.objects.get(user=user)
    leaderboard_entry.xp = 0
    leaderboard_entry.quiz_count = 0
    leaderboard_entry.save()

    responce = client.get(url, follow=True)

    leaderboard_entry = Leaderboard.objects.get(user=user)

    assert responce.status_code == 200
    assert leaderboard_entry.xp == int(100 / (0 + 4))
    assert leaderboard_entry.quiz_count == 1


@pytest.mark.django_db
def test_search_view_unauthenticated(client, user):
    url = reverse('accounts:xp', args=[user.username])
    responce = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(responce, next)
