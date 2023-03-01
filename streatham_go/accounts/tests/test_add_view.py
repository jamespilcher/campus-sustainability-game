import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from urllib.parse import urlencode

pytest.USER_PASSWORD = '12345'
pytest.USER_WRONG_PASSWORD = 'wrong_password'


@pytest.fixture
@pytest.mark.django_db
def user() -> User:
    u = User.objects.create_user('ethanhofton',
                                 'eh736@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'Ethan'
    u.last_name = 'Hofton'
    u.save()

    return u


@pytest.mark.django_db
def test_add_view(user, client):
    pass


@pytest.mark.django_db
def test_add_view_sef(user, client):
    pass


@pytest.mark.django_db
def test_add_view_non_existant(user, client):
    pass


@pytest.mark.django_db
def test_add_view_allready_friends(user, client):
    pass


def test_add_view_unauthenticated(client):
    url = reverse('accounts:add', kwargs={'username': 'user'})
    responce = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(responce, next)
