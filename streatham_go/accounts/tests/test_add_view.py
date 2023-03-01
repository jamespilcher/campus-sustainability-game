import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from urllib.parse import urlencode
from ..models import Friend

pytest.USER_PASSWORD = '12345'
pytest.USER_WRONG_PASSWORD = 'wrong_password'


@pytest.fixture
@pytest.mark.django_db
def user1() -> User:
    u = User.objects.create_user('ethanone',
                                 'ethanone@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'ethan'
    u.last_name = 'one'
    u.save()

    return u


@pytest.fixture
@pytest.mark.django_db
def user2() -> User:
    u = User.objects.create_user('ethantwo',
                                 'ethantwo@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'ethan'
    u.last_name = 'two'
    u.save()

    return u


@pytest.mark.django_db
def test_add_view(user1, user2, client):
    client.login(username=user1.username, password=pytest.USER_PASSWORD)
    url = reverse('accounts:add', kwargs={'username': user2.username})
    responce = client.get(url, follow=True)

    assert responce.status_code == 200
    assert (Friend.objects.filter(user1=user1,
                                  user2=user2).exists() or
            Friend.objects.filter(user1=user2,
                                  user2=user1).exists())


@pytest.mark.django_db
def test_add_view_self(user1, client):
    client.login(username=user1.username, password=pytest.USER_PASSWORD)
    url = reverse('accounts:add', kwargs={'username': user1.username})
    responce = client.get(url, follow=True)

    assert responce.status_code == 406
    assert not Friend.objects.filter(user1=user1,
                                     user2=user1).exists()


@pytest.mark.django_db
def test_add_view_non_existant(user1, user2, client):
    client.login(username=user1.username, password=pytest.USER_PASSWORD)
    url = reverse('accounts:add', kwargs={'username': user2.username + 'not'})
    responce = client.get(url, follow=True)

    assert responce.status_code == 404


@pytest.mark.django_db
def test_add_view_allready_friends(user1, user2, client):
    f = Friend(user1=user1, user2=user2)
    f.save()

    client.login(username=user1.username, password=pytest.USER_PASSWORD)
    url = reverse('accounts:add', kwargs={'username': user2.username})
    responce = client.get(url, follow=True)

    assert responce.status_code == 406
    assert not (Friend.objects.filter(user1=user1,
                                      user2=user2).exists() and
                Friend.objects.filter(user1=user2,
                                      user2=user1).exists())


def test_add_view_unauthenticated(client):
    url = reverse('accounts:add', kwargs={'username': 'user'})
    responce = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(responce, next)
