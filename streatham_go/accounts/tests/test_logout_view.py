import pytest
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.test import TestCase


@pytest.fixture
def user() -> User:
    u = User.objects.create_user('ethanhofton',
                                 'eh736@exeter.ac.uk',
                                 '12345')
    u.first_name = 'Ethan'
    u.last_name = 'Hofton'
    u.save()

    return u


@pytest.mark.django_db
def test_logout_view_logout(user, client):
    client.login(username=user.username, password='12345')

    url = reverse('accounts:logout')
    responce = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'logout': True})

    assert responce.status_code == 200
    assert not responce.context['user'].is_authenticated
    TestCase().assertRedirects(responce, next)


def test_logout_view_unauthenticated(client):
    url = reverse('accounts:logout')
    responce = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(responce, next)
