import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase

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


@pytest.mark.django_db
def test_login_view_authenticated(user, client):
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    url = reverse('accounts:login')
    responce = client.get(url, follow=True)
    next = reverse('app:home')

    TestCase().assertRedirects(responce, next)
