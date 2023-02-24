import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from ..tokens import email_verification_token
from urllib.parse import urlencode

pytest.USER_PASSWORD = '12345'


@pytest.fixture
def user() -> User:
    u = User.objects.create_user('ethanhofton',
                                 'eh736@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'Ethan'
    u.last_name = 'Hofton'
    u.save()

    return u


@pytest.fixture
def user2() -> User:
    u = User.objects.create_user('admin',
                                 'streathamgo@gmail.com',
                                 pytest.USER_PASSWORD)
    u.first_name = 'Streatham'
    u.last_name = 'Go'
    u.save()

    return u


@pytest.mark.django_db
def test_activate_view_authenticated(user, client):
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    url = reverse('accounts:login')
    responce = client.get(url, follow=True)
    next = reverse('app:home')

    TestCase().assertRedirects(responce, next)


@pytest.mark.django_db
def test_activate_view_wrong_username(user, client):
    url = reverse('accounts:activate',
                  kwargs={'username': user.username + '_incorect'})
    responce = client.get(url)

    assert responce.status_code == 200
    assert (responce.context.get("user_not_found"))


@pytest.mark.django_db
def test_activate_view_wrong_token(user, client):
    user.is_active = False
    user.save()

    url = reverse('accounts:activate',
                  kwargs={'username': user.username})
    url += '?' + urlencode({'token': 'wrong_token'})

    responce = client.get(url)
    user = User.objects.get(pk=user.pk)

    assert responce.status_code == 200
    assert responce.context.get('invalid_token')
    assert not user.is_active


@pytest.mark.django_db
def test_activate_view_valid_token_inactive_user(user, client):
    user.is_active = False
    user.save()

    url = reverse('accounts:activate',
                  kwargs={'username': user.username})
    token = email_verification_token.make_token(user)
    url += '?' + urlencode({'token': token})

    responce = client.get(url)
    user = User.objects.get(pk=user.pk)

    assert responce.status_code == 200
    assert responce.context.get('success')
    assert user.is_active


@pytest.mark.django_db
def test_activate_view_valid_token_wrong_user(user, user2, client):
    user2_token = email_verification_token.make_token(user2)

    user.is_active = False
    user.save()

    url = reverse('accounts:activate',
                  kwargs={'username': user.username})
    url += '?' + urlencode({'token': user2_token})

    responce = client.get(url)
    user = User.objects.get(pk=user.pk)

    assert responce.status_code == 200
    assert responce.context.get('invalid_token')
    assert not user.is_active


@pytest.mark.django_db
def test_activate_view_valid_token_active_user(user, client):
    user.is_active = False
    user.save()

    url = reverse('accounts:activate',
                  kwargs={'username': user.username})
    token = email_verification_token.make_token(user)
    url += '?' + urlencode({'token': token})

    user.is_active = True
    user.save()

    responce = client.get(url)
    user = User.objects.get(pk=user.pk)

    assert responce.status_code == 200
    assert responce.context.get('invalid_token')
