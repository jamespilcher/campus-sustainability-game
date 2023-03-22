import pytest
from django.urls import reverse
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
    # set the first
    u.first_name = 'Ethan'
    # set the last name
    u.last_name = 'Hofton'
    # save the user
    u.save()

    # return the user
    return u


@pytest.mark.django_db
# test the register view when authenticated
def test_register_view_authenticated(user, client):
    """
        Test the register view when authenticated

        check that the user is redirected to the home page
        when they are already authenticated and try to access the
        register view
    """
    # login the user
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    # get the url
    url = reverse('accounts:register')
    # get the response
    responce = client.get(url, follow=True)
    # store the next url
    next = reverse('app:home')

    # check that the responce redirects to the next url
    TestCase().assertRedirects(responce, next)


@pytest.mark.django_db
# test the register view with a successful registration
def test_register_view_success(client):
    """
        Test the register view with a successful registration

        check that the user is redirected to the home page
        when they successfully register
    """
    # get the url
    url = reverse('accounts:register')
    # get the response
    responce = client.post(url, {
                               'f_name': 'new',
                               'l_name': 'user',
                               'username': 'newuser',
                               'password': pytest.USER_PASSWORD,
                               'rpassword': pytest.USER_PASSWORD,
                               'email': 'newuser'
                           }, follow=True)

    # login the client
    logged_in = client.login(username='newuser', password=pytest.USER_PASSWORD)

    # check the status code is 200
    assert responce.status_code == 200
    # check that the redirect chain is 1
    assert len(responce.redirect_chain) == 1
    # check that the user is logged in
    assert logged_in

    # check the newly created user exists
    user = User.objects.get(username='newuser')
    # check the user is not active
    assert not user.is_active


# test data for the invalid form
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
# paramiterize the test so it can be run with all the test cases
@pytest.mark.parametrize("f_name,l_name,username,password,rpassword,email",
                         test_data)
# test the register view with an invalid form
def test_register_view_invalid_form(user,
                                    client,
                                    f_name,
                                    l_name,
                                    username,
                                    password,
                                    rpassword,
                                    email):
    """
        Test the register view with an invalid form

        check that the user is not redirected to the home page
        when they try to register with an invalid form. Check
        that the user is not created.
    """
    # get the url
    url = reverse('accounts:register')
    # get the response with the test data
    responce = client.post(url, {
                               'f_name': f_name,
                               'l_name': l_name,
                               'username': username,
                               'password': password,
                               'rpassword': rpassword,
                               'email': email,
                           }, follow=True)

    # check the status code is 200
    assert responce.status_code == 200
    # check that the redirect chain is 0
    assert len(responce.redirect_chain) == 0
    # check the users was not created
    assert not User.objects.filter(username=username, email=email).exists()
