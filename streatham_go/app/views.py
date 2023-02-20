from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'app/index.html')


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'app/profile.html')


@login_required(login_url='/login/')
def home(request):
    return render(request, 'app/home.html')


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('app:login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    context = {}
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            if request.GET.get('next') is not None:
                return redirect(request.GET['next'])

            return redirect("app:home")
        else:
            context["error_message"] = "Username Or Password Is Incorrect"
    elif request.method == 'GET':
        if request.GET.get('next') is not None:
            context['next'] = '?next=' + request.GET['next']

    return render(request, 'app/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    context = {}
    error_message = ""
    if request.method == 'POST':
        f_name = request.POST["f_name"]
        l_name = request.POST["l_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        rpassword = request.POST["rpassword"]

        context["f_name"] = f_name
        context["l_name"] = l_name
        context["username"] = username
        context["email"] = email

        if not f_name:
            error_message = "Please Enter Your First Name"
        elif not l_name:
            error_message = "Please Enter Your Last Name"
        elif not username:
            error_message = "Please Enter Your Username"
        elif not email:
            error_message = "Please Enter Your Email"
        elif not password:
            error_message = "Please Enter A Password"
        elif not rpassword:
            error_message = "Please Repete Your Password"
        elif not (rpassword == password):
            error_message = "Passwords Don't match"
        elif User.objects.filter(username=username).exists():
            error_message = "Username Taken, please pick another"
            context["username"] = ""
        else:
            email = email + '@exeter.ac.uk'
            user = User.objects.create_user(username, email, password)
            if not user:
                error_message = "Failed to create User"
            else:
                user.first_name = f_name
                user.last_name = l_name
                user.save()
                return redirect('app:login')

    context["error_message"] = error_message

    return render(request, 'app/register.html', context)
