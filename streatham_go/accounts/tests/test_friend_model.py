import pytest
from django.contrib.auth.models import User
from ..models import Friend

pytest.USER_PASSWORD = '12345'
pytest.USER_WRONG_PASSWORD = 'wrong_password'


@pytest.fixture
@pytest.mark.django_db
def user1() -> User:
    u = User.objects.create_user('ethanhofton',
                                 'eh736@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'Ethan'
    u.last_name = 'Hofton'
    u.save()

    return u


@pytest.fixture
@pytest.mark.django_db
def user2() -> User:
    u = User.objects.create_user('testuser',
                                 'testuser@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    u.first_name = 'Test'
    u.last_name = 'User'
    u.save()

    return u


@pytest.mark.django_db
def test_friend_are_friends_true_user1_first(user1, user2):
    friend_relation = Friend(user1=user1, user2=user2)
    friend_relation.save()

    assert Friend.are_friends(user1, user2)
    assert Friend.are_friends(user2, user1)


@pytest.mark.django_db
def test_friend_are_friends_true_user1_second(user1, user2):
    friend_relation = Friend(user1=user2, user2=user1)
    friend_relation.save()

    assert Friend.are_friends(user1, user2)
    assert Friend.are_friends(user2, user1)


@pytest.mark.django_db
def test_friend_are_friends_false(user1, user2):
    assert not Friend.are_friends(user1, user2)
    assert not Friend.are_friends(user2, user1)


@pytest.mark.django_db
def test_friend_is_self_true(user1, user2):
    assert Friend.is_self(user1, user1)
    assert Friend.is_self(user2, user2)


@pytest.mark.django_db
def test_friend_is_self_false(user1, user2):
    assert not Friend.is_self(user1, user2)
    assert not Friend.is_self(user2, user1)


@pytest.mark.django_db
def test_friend_get_friends_none(user1, user2):
    assert len(Friend.get_friends(user1)) == 0
    assert len(Friend.get_friends(user2)) == 0


@pytest.mark.django_db
def test_friend_get_friends(user1, user2):
    friend_relation = Friend(user1=user2, user2=user1)
    friend_relation.save()
    assert len(Friend.get_friends(user1)) == 1
    assert len(Friend.get_friends(user2)) == 1
    assert Friend.get_friends(user1) == [user2]
    assert Friend.get_friends(user2) == [user1]
