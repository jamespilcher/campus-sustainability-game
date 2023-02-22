from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.urls import reverse
from urllib.parse import urlencode


@login_required
def logout_view(request):
    logout(request)
    base_redirect_url = reverse('app:login')
    qurey_string = urlencode({'logout': True})
    url = '{}?{}'.format(base_redirect_url, qurey_string)
    return redirect(url)
