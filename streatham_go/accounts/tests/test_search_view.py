import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from urllib.parse import urlencode
import json

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
def test_search_view_noquery(user1, user2, client):
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    url = reverse('accounts:search')
    responce = client.get(url, follow=True)

    assert responce.status_code == 200
    assert responce.context["users"] == []


@pytest.mark.django_db
def test_search_view_ajax_request(user1, client):
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    url = reverse('accounts:search')
    responce = client.get(url, follow=True, **{'HTTP_X_REQUESTED_WITH':
                          'XMLHttpRequest'})
    jsonResponce = json.loads(responce.content)

    assert responce.status_code == 200
    assert jsonResponce["html_from_view"]


@pytest.mark.django_db
def test_search_view_ajax_request_no_users_if_blank_query(user1,
                                                          user2,
                                                          client):
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    url = reverse('accounts:search')
    responce = client.get(url, {'q': ''}, follow=True,
                          **{'HTTP_X_REQUESTED_WITH':
                          'XMLHttpRequest'})
    jsonResponce = json.loads(responce.content)

    print(jsonResponce)
    assert responce.status_code == 200
    assert jsonResponce["html_from_view"]
    assert not (user1.username in jsonResponce["html_from_view"])
    assert not (user2.username in jsonResponce["html_from_view"])


@pytest.mark.django_db
def test_search_view_ajax_request_check_users(user1, user2, client):
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    url = reverse('accounts:search')
    responce = client.get(url, {'q': 'ethan'}, follow=True,
                          **{'HTTP_X_REQUESTED_WITH':
                          'XMLHttpRequest'})
    jsonResponce = json.loads(responce.content)

    print(jsonResponce)
    assert responce.status_code == 200
    assert jsonResponce["html_from_view"]
    assert user1.username in jsonResponce["html_from_view"]
    assert user2.username in jsonResponce["html_from_view"]


@pytest.mark.django_db
def test_search_view_ajax_request_check_users_not_in_results(user1,
                                                             user2,
                                                             client):
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    url = reverse('accounts:search')
    responce = client.get(url, {'q': 'randomuser'}, follow=True,
                          **{'HTTP_X_REQUESTED_WITH':
                          'XMLHttpRequest'})
    jsonResponce = json.loads(responce.content)

    print(jsonResponce)
    assert responce.status_code == 200
    assert jsonResponce["html_from_view"]
    assert not (user1.username in jsonResponce["html_from_view"])
    assert not (user2.username in jsonResponce["html_from_view"])


@pytest.mark.django_db
def test_search_view_unauthenticated(client):
    url = reverse('accounts:search')
    responce = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(responce, next)
