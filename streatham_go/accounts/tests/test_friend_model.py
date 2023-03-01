import pytest
from django.contrib.auth.models import User

pytest.USER_PASSWORD = '12345'
pytest.USER_WRONG_PASSWORD = 'wrong_password'


@pytest.fixture
@pytest.mark.django_db
def user() -> User:
    u = User.objects.create_user('ethanhofton',
                                 'eh736@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'Ethan'
    u.last_name = 'Hofton'
    u.save()

    return u


@pytest.mark.django_db
def test_friend_are_friends_true(user, client):
    pass


@pytest.mark.django_db
def test_friend_are_friends_false(user, client):
    pass


@pytest.mark.django_db
def test_friend_is_self_true(user, client):
    pass


@pytest.mark.django_db
def test_friend_is_self_false(user, client):
    pass


@pytest.mark.django_db
def test_friend_get_friends_none(user, client):
    pass


@pytest.mark.django_db
def test_friend_get_friends_one(user, client):
    pass


@pytest.mark.django_db
def test_friend_get_friends_two(user, client):
    pass
