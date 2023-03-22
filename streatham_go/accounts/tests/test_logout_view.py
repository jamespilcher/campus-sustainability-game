import pytest
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.test import TestCase

# store the corret password in a global variable
pytest.USER_PASSWORD = '12345'


@pytest.fixture
# create a user fixture
def user() -> User:
    """
        Create a user fixture

        Returns:
            User: The user
    """
    # create a user
    u = User.objects.create_user('ethanhofton',
                                 'eh736@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    # set the first and last name
    u.first_name = 'Ethan'
    u.last_name = 'Hofton'
    # save the user
    u.save()

    # return the user
    return u


@pytest.mark.django_db
# test the logout view works
def test_logout_view_logout(user, client):
    """
        Test the logout view works

        check that the user gets logged out
    """
    # login the user
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    # get the url
    url = reverse('accounts:logout')
    # get the response
    responce = client.get(url, follow=True)
    # get the next url
    next = reverse('accounts:login') + '?' + urlencode({'logout': True})

    # check that the responce redirects to the next url
    assert responce.status_code == 200
    # assert the user is not authenticated (logged out)
    assert not responce.context['user'].is_authenticated
    # check that the responce redirects to the next url
    TestCase().assertRedirects(responce, next)


# test the logout view when the user is not authenticated
def test_logout_view_unauthenticated(client):
    """
        Test the logout view when the user is not authenticated

        check that the user gets redirected to the login page
        when they are not authenticated
    """
    # get the url
    url = reverse('accounts:logout')
    # get the response
    responce = client.get(url, follow=True)
    # get the next url
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    # check that the responce redirects to the next url
    TestCase().assertRedirects(responce, next)
