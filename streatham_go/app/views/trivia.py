from django.shortcuts import render


def trivia(request):
    return render(request, 'app/trivia.html')
