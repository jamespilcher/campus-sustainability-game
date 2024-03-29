import pytest
from django.urls import reverse
from urllib.parse import urlencode
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Location, Game

# Set some user passwords for testing purposes
pytest.USER_PASSWORD = '12345'
pytest.USER_WRONG_PASSWORD = 'wrong_password'


# Define a fixture to create a user for testing purposes
@pytest.fixture
def user() -> User:
    u = User.objects.create_user('jamespilcher',
                                 'jp910@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'James'
    u.last_name = 'Pilcher'
    u.save()
    return u


# Define a fixture to create a user for testing purposes
@pytest.fixture
def game() -> Game:
    g = Game()
    g.file = 'tictactoe.html'
    g.name = 'Tic Tac Toe'
    g.save()
    return g


# Test case for when user is authenticated
@pytest.mark.django_db
def test_home_view_authenticated(user, client):
    client.login(username=user.username, password=pytest.USER_PASSWORD)
    url = reverse('app:home')
    response = client.get(url, follow=True)
    # Make sure 200 OK and no redirects
    assert response.status_code == 200
    assert len(response.redirect_chain) == 0


# Test case for when user is not authenticated
def test_home_view_unauthenticated(client):
    url = reverse('app:home')
    response = client.get(url, follow=True)
    # Make sure the user is redirected to the login page
    next = reverse('accounts:login') + '?' + urlencode({'next': url})
    TestCase().assertRedirects(response, next)


# Test case when user logged in and there are locations in DB
@pytest.mark.django_db
def test_home_view_with_location(client, user, game):
    # Login the user
    client.login(username=user.username, password=pytest.USER_PASSWORD)
    # Create some location objects and save them to the database
    buildings = [
        Location.objects.create(name="Building 1",
                                latitude="50.0",
                                longitude="50.0",
                                message="Come to building 1",
                                icon="null",
                                game=game),

        Location.objects.create(name="Building 2",
                                latitude="50.0",
                                longitude="50.0",
                                message="Come to building 2",
                                icon="null",
                                game=game),
        Location.objects.create(name="Building 3",
                                latitude="50.0",
                                longitude="50.0",
                                message="Come to building 3",
                                game=game,
                                icon="null")
        ]

    for building in buildings:
        building.save()

    # Make sure 200 OK is returned and no redirects
    url = reverse('app:home')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert len(response.redirect_chain) == 0

    # check if locations are present in the context (not empty)
    assert 'locations' in response.context

    assert 'GOOGLE_API_KEY' in response.context


# Test case when user logged in and there are no locations in DB
@pytest.mark.django_db
def test_home_view_no_locations_or_questions(client, user):
    client.login(username=user.username, password=pytest.USER_PASSWORD)

    # Clear all locations from the database
    Location.objects.all().delete()

    # Make a GET request to the home view
    url = reverse('app:home')
    response = client.get(url)

    # Check that the response status code is 200
    assert response.status_code == 200

    # Check that the response contains an error message
    assert ("Found no locations in database. "
            "Please add some locations "
            "in the admin panel.") in str(response.content)
