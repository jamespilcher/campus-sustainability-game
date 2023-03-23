from django.urls import reverse
from urllib.parse import urlencode
from django.test import TestCase


# test the profile view when the user is not authenticated
def test_profile_view_unauthenticated(client):
    """
        Test the profile view when the user is not authenticated

        check that the user is redirected to the login page
        when they are not authenticated
    """
    # get the url
    url = reverse('accounts:profile', kwargs={'username': 'user'})
    # get the responce
    responce = client.get(url, follow=True)
    # set the next url
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    # check that the responce redirects to the next url
    TestCase().assertRedirects(responce, next)
