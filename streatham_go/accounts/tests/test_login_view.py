import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase

pytest.USER_PASSWORD = '12345'
pytest.USER_WRONG_PASSWORD = 'wrong_password'


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
def test_login_view_success(user, client):
    url = reverse('accounts:login')
    responce = client.post(url, {
                               'username': user.username,
                               'password': pytest.USER_PASSWORD
                           }, follow=True)

    assert responce.status_code == 200
    assert responce.context['user'].is_authenticated
    assert responce.context['user'].username == user.username
    assert responce.context['user'].email == user.email
    assert responce.context['user'].password == user.password
    assert responce.context['user'].first_name == user.first_name
    assert responce.context['user'].last_name == user.last_name
    TestCase().assertRedirects(responce, reverse('app:home'))


@pytest.mark.django_db
def test_login_view_fail(user, client):
    url = reverse('accounts:login')
    responce = client.post(url, {
                               'username': user.username,
                               'password': pytest.USER_WRONG_PASSWORD
                           })

    assert responce.status_code == 200
    assert not responce.context['user'].is_authenticated
    assert responce.context['error']


@pytest.mark.django_db
def test_login_view_success_next(user, client):
    next = reverse('accounts:profile')
    url = reverse('accounts:login')

    responce = client.post(url, {
                               'username': user.username,
                               'password': pytest.USER_PASSWORD,
                               'next': next,
                           }, follow=True)

    assert responce.status_code == 200
    assert responce.context['user'].is_authenticated
    assert responce.context['user'].username == user.username
    assert responce.context['user'].email == user.email
    assert responce.context['user'].password == user.password
    assert responce.context['user'].first_name == user.first_name
    assert responce.context['user'].last_name == user.last_name
    TestCase().assertRedirects(responce, next)


@pytest.mark.django_db
def test_login_view_authenticated(user, client):
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    url = reverse('accounts:login')
    responce = client.get(url, follow=True)
    next = reverse('app:home')

    TestCase().assertRedirects(responce, next)
