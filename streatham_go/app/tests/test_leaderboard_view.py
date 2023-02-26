import pytest
from django.urls import reverse
from urllib.parse import urlencode
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Leaderboard


pytest.USER_PASSWORD = '12345'


@pytest.fixture
def user() -> User:
    u = User.objects.create_user('testUser',
                                 'testUser@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'test'
    u.last_name = 'user'
    u.save()

    return u


@pytest.mark.django_db
def test_leaderboard_view_with_users(client, user):
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    # create three users with different levels
    user_1 = User.objects.create_user(
        'user1',
        'user1@example.com',
        pytest.USER_PASSWORD
    )
    user_2 = User.objects.create_user(
        'user2',
        'user2@example.com',
        pytest.USER_PASSWORD
    )
    user_3 = User.objects.create_user(
        'user3',
        'user3@example.com',
        pytest.USER_PASSWORD
    )
    leaderboard_data = [
        Leaderboard.objects.create(user=user_1, level=2, quiz_count=0),
        Leaderboard.objects.create(user=user_2, level=3, quiz_count=1),
        Leaderboard.objects.create(user=user_3, level=4, quiz_count=2),
        Leaderboard.objects.create(user=user)

    ]

    # test leaderboard view
    url = reverse('app:leaderboard')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert len(response.redirect_chain) == 0

    # check if leaderboard data is present in the context (not empty)
    assert 'globalLeaderboard' in response.context
    assert 'user_data' in response.context
    assert 'current_user_data' in response.context
    assert 'current_user_rank' in response.context

    # check if the leaderboard data is correct
    # should be four users in globalLeaderboard and user_data
    assert response.context['globalLeaderboard'].count() == 4
    assert len(response.context['user_data']) == 4

    # current user should be fourth in the list as they have the lowest level
    assert response.context['current_user_data'] == leaderboard_data[3]
    assert response.context['current_user_rank'] == 4

    # check the user_data list is sorted correctly
    expected_user_data = [
        {'username': 'user3', 'level': 4, 'quiz_count': 2},
        {'username': 'user2', 'level': 3, 'quiz_count': 1},
        {'username': 'user1', 'level': 2, 'quiz_count': 0},
        {'username': 'testUser', 'level': 1, 'quiz_count': 0}
    ]
    assert response.context['user_data'] == expected_user_data


def test_leaderboard_view_unauthenticated(client):
    url = reverse('app:leaderboard')
    response = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(response, next)


@pytest.mark.django_db
def test_leaderboard_view_authenticated(user, client):
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    url = reverse('app:leaderboard')
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert len(response.redirect_chain) == 0
