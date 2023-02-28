from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def search(request):
    return render(request, 'accounts/search.html')
