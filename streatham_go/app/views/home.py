# import datetime
# import random
from django.conf import settings
from django.shortcuts import render
from app.models import Location
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers


@login_required
def home(request):
    context = {}
    if Location.objects.count() == 0:
        messages.error(request, ("Found no locations in database. "
                                 "Please add some locations in the "
                                 "admin panel."))
    else:
        locations = serializers.serialize("json", Location.objects.all())
        context = {
            'locations': locations,
            'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
        }
    return render(request, 'app/home.html', context)
