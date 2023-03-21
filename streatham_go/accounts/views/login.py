from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from ..forms import LoginForm
from ..decorators import anonymous_required


# add the anonymous required decorator
@anonymous_required
# login view function
def login_view(request):
    # initalize the context variable
    context = {}
    # check if the request method is POST
    if request.method == 'POST':
        # get the form data
        form = LoginForm(request.POST)

        # check if the form is valid
        if form.is_valid():
            # get the username and password from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                # check if the user is active
                if not user.is_active:
                    # if the user is not active, set the error message
                    context["inactive"] = True
                else:
                    # if the user is active, login the user
                    login(request, user)

                    # check if the next parameter is set
                    if request.POST.get('next') is not None:
                        # if the next parameter is set, redirect to the next
                        if request.POST['next']:
                            return redirect(request.POST['next'])

                    # redirect to the home page
                    return redirect("app:home")
            else:
                # if the user is not authenticated, set the error message
                context["error"] = True
                # set the form
                if request.POST.get('next') is not None:
                    # if the next parameter is set, reset next parameter
                    context['next'] = request.POST['next']
    elif request.method == 'GET':
        # if the request method is GET, set the form
        form = LoginForm()
        # check if register_success parameter is set
        if request.GET.get('register_success') is not None:
            # if the register_success parameter is set, set the success
            context['register_success'] = request.GET['register_success']
        # check if logout parameter is set
        if request.GET.get('logout') is not None:
            # if the logout parameter is set, set the logout
            context['logout'] = request.GET['logout']
        # check if next parameter is set
        if request.GET.get('next') is not None:
            # if the next parameter is set, set the next
            context['next'] = request.GET['next']
        # check if dev_url parameter is set
        if request.GET.get('dev_url') is not None:
            # if the dev_url parameter is set, set the dev_url
            context['dev_url'] = request.GET['dev_url']

    # set the form
    context['form'] = form

    # render the login page
    return render(request, 'accounts/login.html', context)
