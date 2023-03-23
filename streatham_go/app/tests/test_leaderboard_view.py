import pytest
from django.urls import reverse
from urllib.parse import urlencode
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.tokens.email_verification_token import (
     EmailVerificationTokenGenerator)
from ..models import Leaderboard


pytest.USER_PASSWORD = '12345'


# Create a user for use in tests
@pytest.fixture
@pytest.mark.django_db
def user() -> User:
    u = User.objects.create_user('testUser',
                                 'testUser@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'test'
    u.last_name = 'user'
    u.save()

    return u


@pytest.mark.django_db
# Test for viewing the leaderboard page when logged in as a valid user.
def test_leaderboard_view_authenticated(user, client):
    client.login(username=user.username, password=pytest.USER_PASSWORD)
    Leaderboard.objects.create(user=user, level=1)

    url = reverse('app:leaderboard')
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert len(response.redirect_chain) == 0


# Test for viewing the leaderboard page when not logged in.
def test_leaderboard_view_unauthenticated(client):
    url = reverse('app:leaderboard')
    response = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(response, next)


# Test for viewing the leaderboard with users in it
# Tests that users are added and then sorted correctly
@pytest.mark.django_db
def test_leaderboard_view_with_users(client, user):
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    # create three users with different levels, and save them to the db
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
        Leaderboard.objects.create(
            user=user_1, level=3, xp=0, numGamesPlayed=10),
        Leaderboard.objects.create(
            user=user_2, level=3, xp=50, numGamesPlayed=8),
        Leaderboard.objects.create(
            user=user_3, level=2, xp=50, numGamesPlayed=5),
        Leaderboard.objects.create(
            user=user, level=1, xp=50, numGamesPlayed=2)
    ]
    for lb in leaderboard_data:
        lb.save()

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
    # users with higher level should be first
    # users with same level should be sorted by highest xp
    expected_user_data = [
        {'username': 'user2', 'level': 3, 'xp': 50, 'numGamesPlayed': 8},
        {'username': 'user1', 'level': 3, 'xp': 0, 'numGamesPlayed': 10},
        {'username': 'user3', 'level': 2, 'xp': 50, 'numGamesPlayed': 5},
        {'username': 'testUser', 'level': 1, 'xp': 50, 'numGamesPlayed': 2},
    ]
    assert response.context['user_data'] == expected_user_data


# Test to make sure a user is added to the leaderboard only after
# they have activated their account
@pytest.mark.django_db
def test_leaderboard_view_user_added_to_leaderboard_after_activation(
        user, client):
    url = reverse('accounts:register')
    response = client.post(url, {
                               'f_name': 'test',
                               'l_name': 'user',
                               'username': 'testUser',
                               'password': pytest.USER_PASSWORD,
                               'rpassword': pytest.USER_PASSWORD,
                               'email': 'testUser@exeter.ac.uk'
                           }, follow=True)

    # Check the leaderboard is empty; user shouldn't be added as not active
    leaderboard_data = Leaderboard.objects.all()
    assert leaderboard_data.count() == 0

    # Activate the user's account
    user = User.objects.get(username='testUser')
    token = EmailVerificationTokenGenerator().make_token(user)
    print(token)
    activation_url = f'/accounts/{user.username}/activate?token={token}'
    response = client.get(activation_url, follow=True)
    assert response.status_code == 200

    # Check that the user is in the leaderboard
    leaderboard_data = Leaderboard.objects.all()
    assert leaderboard_data.count() == 1
    assert leaderboard_data[0].user == user
