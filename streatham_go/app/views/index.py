from django.shortcuts import render


def index(request):
    # return the landing page
    return render(request, 'app/index.html')
