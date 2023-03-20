from django.shortcuts import render


def crossword(request):
    return render(request, 'app/crossword.html')
