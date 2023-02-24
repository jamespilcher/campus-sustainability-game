from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import urlencode
from ..forms import RegisterForm
from ..decorators import anonymous_required
from app.models import Leaderboard


@anonymous_required
def register(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email'] + '@exeter.ac.uk'
            password = form.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            if not user:
                context['error'] = True
            else:
                user.first_name = f_name
                user.last_name = l_name
                user.save()

                # Create a leaderboard entry for the user
                leaderboard_entry = Leaderboard.objects.create(user=user)

                base_redirect_url = reverse('accounts:login')
                qurey_string = urlencode({'register_success': True})
                url = '{}?{}'.format(base_redirect_url, qurey_string)
                return redirect(url)
    else:
        form = RegisterForm()

    context['form'] = form

    return render(request, 'accounts/register.html', context)
