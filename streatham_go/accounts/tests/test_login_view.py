import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase

# store the corret password in a global variable
pytest.USER_PASSWORD = '12345'
# store the wrong password in a global variable
pytest.USER_WRONG_PASSWORD = 'wrong_password'


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
# test the login view works correctly
def test_login_view_success(user, client):
    """
        Test the login view works correctly

        When a user successfully logs in, they should be redirected to the
        home page.
    """
    # get the url
    url = reverse('accounts:login')
    # get the response
    responce = client.post(url, {
                               'username': user.username,
                               'password': pytest.USER_PASSWORD
                           }, follow=True)

    # check the status code is 200
    assert responce.status_code == 200
    # check the user is authenticated
    assert responce.context['user'].is_authenticated
    # check the user is the correct user
    # check the username is correct
    assert responce.context['user'].username == user.username
    # check the email is correct
    assert responce.context['user'].email == user.email
    # check the password is correct
    assert responce.context['user'].password == user.password
    # check the first name is correct
    assert responce.context['user'].first_name == user.first_name
    # check the last name is correct
    assert responce.context['user'].last_name == user.last_name
    # check the responce redirects to the home page
    TestCase().assertRedirects(responce, reverse('app:home'))


@pytest.mark.django_db
# test the login view fails correctly
def test_login_view_fail(user, client):
    """
        Test the login view fails correctly

        When a user fails to log in, they should be redirected to the login
        page again with an error message. (via the error context variable)
    """
    # get the url
    url = reverse('accounts:login')
    # login with the incorrect password
    responce = client.post(url, {
                               'username': user.username,
                               'password': pytest.USER_WRONG_PASSWORD
                           })

    # check the status code is 200
    assert responce.status_code == 200
    # check the user is not authenticated
    assert not responce.context['user'].is_authenticated
    # check the error message is set
    assert responce.context['error']


@pytest.mark.django_db
# test the login view works correctly with the next parameter
def test_login_view_success_next(user, client):
    """
        Test the login view works correctly with the next parameter

        When a user successfully logs in, they should be redirected to the
        page they were trying to access before they were redirected to the
        login page. (via the next parameter)
    """
    # set the next url
    next = reverse('accounts:profile', kwargs={'username': user.username})
    # get the url
    url = reverse('accounts:login')

    # get the response with the next parameter
    responce = client.post(url, {
                               'username': user.username,
                               'password': pytest.USER_PASSWORD,
                               'next': next,
                           }, follow=True)

    # check the status code is 200
    assert responce.status_code == 200
    # check the user is authenticated
    assert responce.context['user'].is_authenticated
    # check the user is the correct user
    # check the username is correct
    assert responce.context['user'].username == user.username
    # check the email is correct
    assert responce.context['user'].email == user.email
    # check the password is correct
    assert responce.context['user'].password == user.password
    # check the first name is correct
    assert responce.context['user'].first_name == user.first_name
    # check the last name is correct
    assert responce.context['user'].last_name == user.last_name
    # check the responce redirects to the next page
    TestCase().assertRedirects(responce, next)


@pytest.mark.django_db
# test the login view when the user is authenticated
def test_login_view_authenticated(user, client):
    """
        Test the login view when the user is authenticated

        The login view should redirect to the home page
        if a logged in user tries to access it
    """
    # login the user
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    # get the url
    url = reverse('accounts:login')
    # get the response
    responce = client.get(url, follow=True)
    # set the next url
    next = reverse('app:home')

    # check the status code is 200
    TestCase().assertRedirects(responce, next)
