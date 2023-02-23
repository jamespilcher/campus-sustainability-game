import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from urllib.parse import urlencode
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
def test_register_view_authenticated(user, client):
    client.login(username=user.username, password='12345')

    url = reverse('accounts:register')
    responce = client.get(url, follow=True)
    next = reverse('app:home')

    TestCase().assertRedirects(responce, next)


@pytest.mark.django_db
def test_register_view_success(user, client):
    url = reverse('accounts:register')
    responce = client.post(url, {
                               'f_name': 'new',
                               'l_name': 'user',
                               'username': 'newuser',
                               'password': '12345',
                               'rpassword': '12345',
                               'email': 'newuser'
                           }, follow=True)

    next = reverse('accounts:login') + '?' + urlencode(
            {'register_success': True})

    assert responce.status_code == 200
    assert len(responce.redirect_chain) == 1
    TestCase().assertRedirects(responce, next)


test_data = [
    # no firstname
    ("", "lastname", "username", "password", "password", "email"),
    # no lastname
    ("firstname", "", "username", "password", "password", "email"),
    # no email
    ("firstname", "lastname", "", "password", "password", "email"),
    # no password
    ("firstname", "lastname", "username", "", "password", "email"),
    # no repeted password
    ("firstname", "lastname", "username", "password", "", "email"),
    # password missmatch
    ("firstname", "lastname", "username", "password1", "password2", "email"),
    # username taken
    ("firstname", "lastname", "ethanhofton", "password", "password", "email"),
    # email taken
    ("firstname", "lastname", "username", "password", "password", "eh736"),
]


@pytest.mark.django_db
@pytest.mark.parametrize("f_name,l_name,username,password,rpassword,email",
                         test_data)
def test_register_view_invalid_form(user,
                                    client,
                                    f_name,
                                    l_name,
                                    username,
                                    password,
                                    rpassword,
                                    email):
    url = reverse('accounts:register')
    responce = client.post(url, {
                               'f_name': f_name,
                               'l_name': l_name,
                               'username': username,
                               'password': password,
                               'rpassword': rpassword,
                               'email': email,
                           }, follow=True)

    assert responce.status_code == 200
    assert len(responce.redirect_chain) == 0