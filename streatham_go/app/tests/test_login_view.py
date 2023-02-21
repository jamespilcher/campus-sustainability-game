import pytest
from django.urls import reverse
from django.contrib.auth.models import User


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
def test_login_view_success(user, client):
    url = reverse('app:login')
    responce = client.post(url, {
                               'username': user.username,
                               'password': '12345'
                           }, follow=True)

    assert responce.status_code == 200
    assert responce.context['user'].is_authenticated
    assert responce.context['user'].username == user.username
    assert responce.context['user'].email == user.email
    assert responce.context['user'].password == user.password
    assert responce.context['user'].first_name == user.first_name
    assert responce.context['user'].last_name == user.last_name


@pytest.mark.django_db
def test_login_view_fail(user, client):
    url = reverse('app:login')
    responce = client.post(url, {
                               'username': user.username,
                               'password': 'wrong_password'
                           }, follow=True)

    assert responce.status_code == 200
    assert not responce.context['user'].is_authenticated
    assert responce.context['error_message']
