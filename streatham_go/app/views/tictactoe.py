from django.shortcuts import render


def tictactoe(request):
    return render(request, 'app/tictactoe.html')
