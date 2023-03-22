import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from urllib.parse import urlencode
import json

# store the corret password in a global variable
pytest.USER_PASSWORD = '12345'
# store the wrong password in a global variable
pytest.USER_WRONG_PASSWORD = 'wrong_password'


@pytest.fixture
@pytest.mark.django_db
# create a user fixture
def user1() -> User:
    """
        Create a user fixture

        Returns:
            User: The user
    """
    # create a user
    u = User.objects.create_user('ethanone',
                                 'ethanone@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    # set the first and last name
    u.first_name = 'ethan'
    u.last_name = 'one'
    # save the user
    u.save()

    # return the user
    return u


@pytest.fixture
@pytest.mark.django_db
# create a user fixture
def user2() -> User:
    """
        Create a user fixture

        Returns:
            User: The user
    """
    # create a user
    u = User.objects.create_user('ethantwo',
                                 'ethantwo@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    # set the first and last name
    u.first_name = 'ethan'
    u.last_name = 'two'
    # save the user
    u.save()

    # return the user
    return u


@pytest.mark.django_db
# test the search view with no search query
def test_search_view_noquery(user1, user2, client):
    """
        Test the search view with no search query

        check that the search view returns no users when there
        is no search query
    """
    # login the user
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    # get the url
    url = reverse('accounts:search')
    # get the response
    responce = client.get(url, follow=True)

    # assert the status code is 200
    assert responce.status_code == 200
    # assert the context contains the users that is empty
    assert responce.context["users"] == []


@pytest.mark.django_db
# test the search view with a search query
def test_search_view_ajax_request(user1, client):
    """
        Test the search view with an ajax request

        check the view returns json when the request is ajax
    """
    # login the user
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    # get the url
    url = reverse('accounts:search')
    # get the response with ajax headers
    responce = client.get(url, follow=True, **{'HTTP_X_REQUESTED_WITH':
                          'XMLHttpRequest'})
    # get the json responce
    jsonResponce = json.loads(responce.content)

    # assert the status code is 200
    assert responce.status_code == 200
    # assert the context contains html_from_view filed that is not empty
    assert jsonResponce["html_from_view"]


@pytest.mark.django_db
# test the search view with an empty search query that returns no users
def test_search_view_ajax_request_no_users_if_blank_query(user1,
                                                          user2,
                                                          client):
    """
        Test the search view with an ajax request and an empty search query

        check the view returns no users when the search query is empty
    """
    # login the user
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    # get the url
    url = reverse('accounts:search')
    # get the response with ajax headers and an empty search query
    responce = client.get(url, {'q': ''}, follow=True,
                          **{'HTTP_X_REQUESTED_WITH':
                          'XMLHttpRequest'})
    # get the json responce
    jsonResponce = json.loads(responce.content)

    # assert the status code is 200
    assert responce.status_code == 200
    # assert the context contains html_from_view filed that is not empty
    assert jsonResponce["html_from_view"]
    # check user1 is not in the responce
    assert not (user1.username in jsonResponce["html_from_view"])
    # check user 2 is not in the responce
    assert not (user2.username in jsonResponce["html_from_view"])


@pytest.mark.django_db
# test the search view with a search query that returns the correct users
# the search query contains a search for both users
def test_search_view_ajax_request_check_users(user1, user2, client):
    """
        Test the search view with an ajax request and a search query

        check the view returns the correct users when the search query
        contains both users
    """
    # login the user
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    # get the url
    url = reverse('accounts:search')
    # get the response with ajax headers and a search query for ethan
    responce = client.get(url, {'q': 'ethan'}, follow=True,
                          **{'HTTP_X_REQUESTED_WITH':
                          'XMLHttpRequest'})
    # get the json responce
    jsonResponce = json.loads(responce.content)

    # assert the status code is 200
    assert responce.status_code == 200
    # assert the context contains html_from_view filed that is not empty
    assert jsonResponce["html_from_view"]
    # check user1 is in the responce
    assert user1.username in jsonResponce["html_from_view"]
    # check user 2 is in the responce
    assert user2.username in jsonResponce["html_from_view"]


@pytest.mark.django_db
# test the search view with a search query that returns the correct users
# the search query will have no results
def test_search_view_ajax_request_check_users_not_in_results(user1,
                                                             user2,
                                                             client):
    """
        Test the search view with an ajax request and a search query

        check the view returns the correct users when the search query
        contains no users
    """
    # login the user
    client.login(username=user1.username, password=pytest.USER_PASSWORD)

    # get the url
    url = reverse('accounts:search')
    # get the response with ajax headers and a search query for random user
    responce = client.get(url, {'q': 'randomuser'}, follow=True,
                          **{'HTTP_X_REQUESTED_WITH':
                          'XMLHttpRequest'})
    # get the json responce
    jsonResponce = json.loads(responce.content)

    # assert the status code is 200
    assert responce.status_code == 200
    # assert the context contains html_from_view filed that is not empty
    assert jsonResponce["html_from_view"]
    # check user1 is not in the responce
    assert not (user1.username in jsonResponce["html_from_view"])
    # check user 2 is not in the responce
    assert not (user2.username in jsonResponce["html_from_view"])


@pytest.mark.django_db
# test the search view for an unauthenticated user
def test_search_view_unauthenticated(client):
    """
        Test the search view for an unauthenticated user

        check the view redirects to the login page when the user is
        unauthenticated
    """
    # get the url
    url = reverse('accounts:search')
    # get the response
    responce = client.get(url, follow=True)
    # get the next url
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    # check the responce redirects to the login page
    TestCase().assertRedirects(responce, next)
