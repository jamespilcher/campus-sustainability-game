import pytest
from django.contrib.auth.models import User
from ..models import Friend

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
    u = User.objects.create_user('testuser',
                                 'testuser@exeter.ac.uk',
                                 pytest.USER_PASSWORD)
    # set the first and last name
    u.first_name = 'Test'
    u.last_name = 'User'
    # save the user
    u.save()

    # return the user
    return u


@pytest.mark.django_db
# test the are_friends class method
def test_friend_are_friends_true_user1_first(user1, user2):
    """
        Test the are_friends class method

        When two users are friends, the are_friends method should return True
        in both directions.
    """
    # create a friend relation with user1 first
    friend_relation = Friend(user1=user1, user2=user2)
    # save the friend relation
    friend_relation.save()

    # check the users are friends
    # check user1 is friends with user2
    assert Friend.are_friends(user1, user2)
    # check user2 is friends with user1
    assert Friend.are_friends(user2, user1)


@pytest.mark.django_db
# test the are_friends class method
def test_friend_are_friends_true_user1_second(user1, user2):
    """
        Test the are_friends class method

        When two users are friends, the are_friends method should return True
        in both directions.
    """
    # create a friend relation with user2 first
    friend_relation = Friend(user1=user2, user2=user1)
    # save the friend relation
    friend_relation.save()

    # check the users are friends
    # check user1 is friends with user2
    assert Friend.are_friends(user1, user2)
    # check user2 is friends with user1
    assert Friend.are_friends(user2, user1)


@pytest.mark.django_db
# test the are_friends class method
def test_friend_are_friends_false(user1, user2):
    """
        Test the are_friends class method

        When two users are not friends, the are_friends method should return
        False in both directions.
    """
    # check the users are not friends
    # check user1 is not friends with user2
    assert not Friend.are_friends(user1, user2)
    # check user2 is not friends with user1
    assert not Friend.are_friends(user2, user1)


@pytest.mark.django_db
# test the friend is_self class method
def test_friend_is_self_true(user1, user2):
    """
        Test the is_self class method

        When two users are the same, the is_self method should return True
    """
    # check the users are the same
    assert Friend.is_self(user1, user1)
    # check the users are the same
    assert Friend.is_self(user2, user2)


@pytest.mark.django_db
# test the friend is_self class method
def test_friend_is_self_false(user1, user2):
    """
        Test the is_self class method

        When two users are not the same, the is_self method should return False
        in both directions.
    """
    # check the users are not the same
    # check user1 is not the same as user2
    assert not Friend.is_self(user1, user2)
    # check user2 is not the same as user1
    assert not Friend.is_self(user2, user1)


@pytest.mark.django_db
# test the friend get_friends class method
def test_friend_get_friends_none(user1, user2):
    """
        Test the get_friends class method

        The get_friends method should return an empty list when the user has
        no friends
    """
    # check the users have no friends
    # check user1 has no friends
    assert len(Friend.get_friends(user1)) == 0
    # check user2 has no friends
    assert len(Friend.get_friends(user2)) == 0


@pytest.mark.django_db
# test the friend get_friends class method
def test_friend_get_friends(user1, user2):
    """
        Test the get_friends class method

        The get_friends method should return a list of the users friends
    """
    # create a friend relation with user1 first
    friend_relation = Friend(user1=user2, user2=user1)
    # save the friend relation
    friend_relation.save()
    # check the users have friends
    # check user1 has one friend
    assert len(Friend.get_friends(user1)) == 1
    # check user2 has one friend
    assert len(Friend.get_friends(user2)) == 1
    # check the users have the correct friends
    # check user1 is friends with user2
    assert Friend.get_friends(user1) == [user2]
    # check user2 is friends with user1
    assert Friend.get_friends(user2) == [user1]
