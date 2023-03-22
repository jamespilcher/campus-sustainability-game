import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from ..tokens import email_verification_token
from urllib.parse import urlencode

# store the corret password in a global variable
pytest.USER_PASSWORD = '12345'


@pytest.fixture
# create a user fixture
def user() -> User:
    # create a user
    u = User.objects.create_user('ethanhofton',
                                 'eh736@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    # set the first and last name
    u.first_name = 'Ethan'
    u.last_name = 'Hofton'
    # save the user
    u.save()

    # return the user
    return u


@pytest.fixture
# create a user fixture
def user2() -> User:
    # create a user
    u = User.objects.create_user('admin',
                                 'streathamgo@gmail.com',
                                 pytest.USER_PASSWORD)
    # set the first and last name
    u.first_name = 'Streatham'
    u.last_name = 'Go'
    # save the user
    u.save()

    # return the user
    return u


@pytest.mark.django_db
# test the activate view when authenticated
def test_activate_view_authenticated(user, client):
    # login the user
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    # get the url
    url = reverse('accounts:login')
    # get the response
    responce = client.get(url, follow=True)
    # get the next url
    next = reverse('app:home')

    # check that the responce redirects to the next url
    TestCase().assertRedirects(responce, next)


@pytest.mark.django_db
# test the activate view with a wrong username
def test_activate_view_wrong_username(user, client):
    # get the url
    url = reverse('accounts:activate',
                  kwargs={'username': user.username + '_incorect'})
    # get the responce
    responce = client.get(url)

    # check that the responce is 200
    assert responce.status_code == 200
    # check that the user_not_found context variable is true
    assert (responce.context.get("user_not_found"))


@pytest.mark.django_db
# test the activate view with a wrong token
def test_activate_view_wrong_token(user, client):
    # set the user activity to false
    user.is_active = False
    # save the user
    user.save()

    # get the url
    url = reverse('accounts:activate',
                  kwargs={'username': user.username})
    # add the wrong token to the url
    url += '?' + urlencode({'token': 'wrong_token'})

    # get the responce
    responce = client.get(url)
    # get the user
    user = User.objects.get(pk=user.pk)

    # check that the responce is 200
    assert responce.status_code == 200
    # check that the invalid_token context variable is true
    assert responce.context.get('invalid_token')
    # check that the user is not active
    assert not user.is_active


@pytest.mark.django_db
# test the activate view with a valid token
def test_activate_view_valid_token_inactive_user(user, client):
    # set the user activity to false
    user.is_active = False
    # save the user
    user.save()

    # get the url
    url = reverse('accounts:activate',
                  kwargs={'username': user.username})
    # get the token
    token = email_verification_token.make_token(user)
    # add the token to the url
    url += '?' + urlencode({'token': token})

    # get the responce
    responce = client.get(url)
    # get the user
    user = User.objects.get(pk=user.pk)

    # check that the responce is 200
    assert responce.status_code == 200
    # check that the success context variable is true
    assert responce.context.get('success')
    # check that the user is active
    assert user.is_active


@pytest.mark.django_db
# test the activate view with a valid token for the wrong user
def test_activate_view_valid_token_wrong_user(user, user2, client):
    # get user2 token
    user2_token = email_verification_token.make_token(user2)

    # set the user activity to false
    user.is_active = False
    # save the user
    user.save()

    # get the url
    url = reverse('accounts:activate',
                  kwargs={'username': user.username})
    # add the token to the url
    url += '?' + urlencode({'token': user2_token})

    # get the responce
    responce = client.get(url)
    # get the user
    user = User.objects.get(pk=user.pk)

    # check that the responce is 200
    assert responce.status_code == 200
    # check that the invalid_token context variable is true
    assert responce.context.get('invalid_token')
    # check that the user is not active
    assert not user.is_active


@pytest.mark.django_db
# test the activate view with a valid token for an active user
def test_activate_view_valid_token_active_user(user, client):
    # set the user activity to true
    user.is_active = False
    # save the user
    user.save()

    # get the url
    url = reverse('accounts:activate',
                  kwargs={'username': user.username})
    # get the token
    token = email_verification_token.make_token(user)
    # add the token to the url
    url += '?' + urlencode({'token': token})

    # set the user activity to true
    user.is_active = True
    # save the user
    user.save()

    # get the responce
    responce = client.get(url)
    # get the user
    user = User.objects.get(pk=user.pk)

    # check that the responce is 200
    assert responce.status_code == 200
    # check that the invalid_token context variable is true
    assert responce.context.get('invalid_token')
