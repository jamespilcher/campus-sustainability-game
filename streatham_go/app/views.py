from django.shortcuts import render


# Create your views here.
def register(request):
    return render(request, 'app/register.html')


def login(request):
    return render(request, 'app/login.html')
