import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from urllib.parse import urlencode
from ..models import Friend

# store the corret password in a global variable
pytest.USER_PASSWORD = '12345'
# store the wrong password in a global variable
pytest.USER_WRONG_PASSWORD = 'wrong_password'


@pytest.fixture
@pytest.mark.django_db
# create a user fixture
def user1() -> User:
    """
        Create a user fixture

        Returns:
            User: The user
    """
    # create a user
    u = User.objects.create_user('ethanone',
                                 'ethanone@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    # set the first and last name
    u.first_name = 'ethan'
    u.last_name = 'one'
    # save the user
    u.save()

    # return the user
    return u


@pytest.fixture
@pytest.mark.django_db
# create a user fixture
def user2() -> User:
    """
        Create a user fixture

        Returns:
            User: The user
    """
    # create a user
    u = User.objects.create_user('ethantwo',
                                 'ethantwo@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    # set the first and last name
    u.first_name = 'ethan'
    u.last_name = 'two'
    # save the user
    u.save()

    # return the user
    return u


@pytest.mark.django_db
# test the add view
def test_add_view(user1, user2, client):
    """
        Test the add view

        check the add view create a friend relation between user1 and
        user2 (order independent)
    """
    # login the user
    client.login(username=user1.username, password=pytest.USER_PASSWORD)
    # get the url
    url = reverse('accounts:add', kwargs={'username': user2.username})
    # get the response
    responce = client.get(url, follow=True)

    # check the status code
    assert responce.status_code == 200
    # check the friend relation exists
    # check either user1 is the first user and user2 is the second user
    # or user2 is the first user and user1 is the second user
    assert (Friend.objects.filter(user1=user1,
                                  user2=user2).exists() or
            Friend.objects.filter(user1=user2,
                                  user2=user1).exists())


@pytest.mark.django_db
# test the add view when user1 tried to add user1 as a friend
def test_add_view_self(user1, client):
    """
        test the add view

        check the add view does not create a friend relation between
        the same user
    """
    # login the user
    client.login(username=user1.username, password=pytest.USER_PASSWORD)
    # get the url
    url = reverse('accounts:add', kwargs={'username': user1.username})
    # get the response
    responce = client.get(url, follow=True)

    # check the status code is 406 (not acceptable)
    assert responce.status_code == 406
    # check the friend relation does not exist
    assert not Friend.objects.filter(user1=user1,
                                     user2=user1).exists()


@pytest.mark.django_db
# test the add view
def test_add_view_non_existant(user1, user2, client):
    """
        test the add view

        check the add view does not create a friend relation between
        user1 and a non-existant user
    """
    # login the user
    client.login(username=user1.username, password=pytest.USER_PASSWORD)
    # get the url (with a non-existant username)
    url = reverse('accounts:add', kwargs={'username': user2.username + 'not'})
    # get the response
    responce = client.get(url, follow=True)

    # check the status code is 404 (not found)
    assert responce.status_code == 404


@pytest.mark.django_db
# test the add view
def test_add_view_allready_friends(user1, user2, client):
    """
        test the add view

        check the add view does not create a friend relation between
        user1 and user2 if they are already friends (order independent)
    """
    # create a friend relation between user1 and user2
    f = Friend(user1=user1, user2=user2)
    # save the friend relation
    f.save()

    # login the user
    client.login(username=user1.username, password=pytest.USER_PASSWORD)
    # get the url
    url = reverse('accounts:add', kwargs={'username': user2.username})
    # get the response
    responce = client.get(url, follow=True)

    # check the status code is 406 (not acceptable)
    assert responce.status_code == 406
    # check the friend relation exists but another isnt created
    assert not (Friend.objects.filter(user1=user1,
                                      user2=user2).exists() and
                Friend.objects.filter(user1=user2,
                                      user2=user1).exists())


# test add view
def test_add_view_unauthenticated(client):
    """
        test the add view

        check the add view redirects to the login page if the user is
        not logged in
    """
    # get the url
    url = reverse('accounts:add', kwargs={'username': 'user'})
    # get the response
    responce = client.get(url, follow=True)
    # set the next url
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    # check the user is redirected to the login page
    TestCase().assertRedirects(responce, next)
