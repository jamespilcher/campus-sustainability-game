from django.shortcuts import render


def wordsearch(request):
    return render(request, 'app/wordsearch.html')
