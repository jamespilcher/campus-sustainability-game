# import datetime
# import random
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.shortcuts import render
from app.models import Location
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# def _generate_building_question():
#     # Seed random number generator with date
#     a = datetime.datetime.now() + datetime.timedelta(days=1)
#     b = a.strftime("%Y%m%d" + settings.SECRET_KEY)  # add django seed
#     random.seed(b)

#     # Select todays random question
#     pks = Question.objects.values_list('pk', flat=True)
#     random_pk = random.choice(pks)
#     random_question = Question.objects.get(pk=random_pk)
#     return random_question


# @login_required
def home(request):
    context = {}
    if Location.objects.count() == 0:
        messages.error(request, ("Found no locations in database. "
                                 "Please add some locations in the "
                                 "admin panel."))
    else:
        locations = Location.objects.all()

        context = {
            'locations': locations,
            'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
        }
    return render(request, 'app/home.html', context)
