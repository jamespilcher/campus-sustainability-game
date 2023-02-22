from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from ..forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                if request.GET.get('next') is not None:
                    return redirect(request.GET['next'])

                return redirect("app:home")
            else:
                context["error_message"] = 'Username or Password Incorrect'
    elif request.method == 'GET':
        form = LoginForm()
        if request.GET.get('register_success') is not None:
            context['register_success'] = request.GET['register_success']
        if request.GET.get('next') is not None:
            context['next'] = '?next=' + request.GET['next']

    context['form'] = form

    return render(request, 'app/login.html', context)
