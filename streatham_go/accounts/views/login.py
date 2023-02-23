from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from ..forms import LoginForm
from ..decorators import anonymous_required


@anonymous_required
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    context["inactive"] = True
                else:
                    login(request, user)

                    if request.POST.get('next') is not None:
                        if request.POST['next']:
                            return redirect(request.POST['next'])

                    return redirect("app:home")
            else:
                context["error"] = True
                if request.POST.get('next') is not None:
                    context['next'] = request.POST['next']
    elif request.method == 'GET':
        form = LoginForm()
        if request.GET.get('register_success') is not None:
            context['register_success'] = request.GET['register_success']
        if request.GET.get('logout') is not None:
            context['logout'] = request.GET['logout']
        if request.GET.get('next') is not None:
            context['next'] = request.GET['next']

    context['form'] = form

    return render(request, 'accounts/login.html', context)
