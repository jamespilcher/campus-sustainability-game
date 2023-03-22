import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Leaderboard
from django.test import TestCase
from urllib.parse import urlencode


# store the corret password in a global variable
pytest.USER_PASSWORD = '12345'
# store the wrong password in a global variable
pytest.USER_WRONG_PASSWORD = 'wrong_password'


# create a user fixture
@pytest.fixture
def user() -> User:
    """
        Create a user fixture

        Returns:
            User: The user
    """
    # create a user
    u = User.objects.create_user('ethanhofton',
                                 'eh736@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    # set the first and last name
    u.first_name = 'Ethan'
    u.last_name = 'Hofton'
    # save the user
    u.save()

    # create a leaderboard entry
    lb_entry = Leaderboard()
    # set the user
    lb_entry.user = u
    # save the leaderboard entry
    lb_entry.save()

    # return the user
    return u


@pytest.mark.django_db
# test the xp view
def test_xp_view_add_xp(user, client):
    """
        Test the xp view

        test the xp view adds the correct ammount of xp
        based on the number of games played
    """
    # login the user
    client.login(username=user.username, password=pytest.USER_PASSWORD)
    # get the url
    url = reverse('accounts:xp', args=[user.username])

    # get the leaderboard entry
    leaderboard_entry = Leaderboard.objects.get(user=user)
    # set the xp and quiz count to 0
    leaderboard_entry.xp = 0
    # set the quiz count to 0
    leaderboard_entry.quiz_count = 0
    # save the leaderboard entry
    leaderboard_entry.save()

    # get the response
    responce = client.get(url, follow=True)

    # get the leaderboard entry
    leaderboard_entry = Leaderboard.objects.get(user=user)

    # assert the response status code is 200
    assert responce.status_code == 200
    # assert the xp is 100 / (0 + 4)
    assert leaderboard_entry.xp == int(100 / (0 + 4))
    # assert the quiz count is 1
    assert leaderboard_entry.quiz_count == 1


@pytest.mark.django_db
# test the xp view
def test_xp_view_level_up(user, client):
    """
        Test the xp view

        Test the xp view increments the level when the xp
        reaches 100
    """
    # login the user
    client.login(username=user.username, password=pytest.USER_PASSWORD)
    # get the url
    url = reverse('accounts:xp', args=[user.username])

    # get the leaderboard entry
    leaderboard_entry = Leaderboard.objects.get(user=user)
    # set the xp and quiz count to 0
    leaderboard_entry.xp = 90
    # set the quiz count to 0
    leaderboard_entry.quiz_count = 0
    # set the level to 1
    leaderboard_entry.level = 1
    # save the leaderboard entry
    leaderboard_entry.save()

    # get the response
    responce = client.get(url, follow=True)

    # get the leaderboard entry
    leaderboard_entry = Leaderboard.objects.get(user=user)

    # assert the response status code is 200
    assert responce.status_code == 200
    # assert the xp is 100 / (0 + 4)
    assert leaderboard_entry.xp == 15
    # assert the quiz count is 1
    assert leaderboard_entry.quiz_count == 1
    # assert the level is 1
    assert leaderboard_entry.level == 2



@pytest.mark.django_db
# test the xp view wehn the user is not logged in
def test_xp_view_unauthenticated(client, user):
    """
        Test the xp view when the user is not logged in

        test the xp view redirects to the login page
        when the user is not logged in
    """
    # get the url
    url = reverse('accounts:xp', args=[user.username])
    # get the response
    responce = client.get(url, follow=True)
    # get the next url
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    # assert that the response redirects to the login page with the next url
    TestCase().assertRedirects(responce, next)
