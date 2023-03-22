from django.shortcuts import render


def privacypolicy(request):
    return render(request, 'accounts/privacypolicy.html')
