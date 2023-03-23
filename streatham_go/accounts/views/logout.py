from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.urls import reverse
from urllib.parse import urlencode


# add the login required decorator
@login_required
# logout view function
def logout_view(request):
    # logout the user
    logout(request)
    # redirect to the login page
    base_redirect_url = reverse('accounts:login')
    # set the logout parameter
    qurey_string = urlencode({'logout': True})
    # redirect to the login page with the logout parameter
    url = '{}?{}'.format(base_redirect_url, qurey_string)
    # redirect to the login page
    return redirect(url)
