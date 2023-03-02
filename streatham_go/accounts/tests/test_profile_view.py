from django.urls import reverse
from urllib.parse import urlencode
from django.test import TestCase


def test_profile_view_unauthenticated(client):
    url = reverse('accounts:profile', kwargs={'username': 'user'})
    responce = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(responce, next)
