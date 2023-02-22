from django.urls import reverse
from urllib.parse import urlencode
from django.test import TestCase


def test_home_view_unauthenticated(client):
    url = reverse('app:home')
    responce = client.get(url, follow=True)
    next = reverse('app:login') + '?' + urlencode({'next': url})

    TestCase().assertRedirects(responce, next)
