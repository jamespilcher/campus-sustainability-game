from django.conf import settings
from django.shortcuts import render, redirect
from app.models import Location
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from ..tokens import generate_game_jwt


@login_required
def home(request):
    # initalize the context variable
    context = {}

    # check if the method is post
    if request.method == 'POST':
        # get the building name from the form
        buildingName = request.POST.get('building')
        # generate the game token
        token = generate_game_jwt(request.user, buildingName)

        # redirect to the play page with the token
        return redirect('app:play', token=token)

    # check if there are any locations in the database
    if Location.objects.count() == 0:
        # if there are no locations, set the error message
        messages.error(request, ("Found no locations in database. "
                                 "Please add some locations in the "
                                 "admin panel."))
    else:
        # if there are locations, get the locations from the database
        locations = serializers.serialize("json", Location.objects.all())
        # set the context variable
        context = {
            'locations': locations,
            'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
        }

    # render the home page
    return render(request, 'app/home.html', context)
