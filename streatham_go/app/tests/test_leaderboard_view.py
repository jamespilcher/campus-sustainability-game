from django.urls import reverse
from urllib.parse import urlencode
from django.test import TestCase


def test_leaderboard_view_unauthenticated(client):
    url = reverse('app:leaderboard')
    responce = client.get(url, follow=True)
    next = reverse('accounts:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(responce, next)
