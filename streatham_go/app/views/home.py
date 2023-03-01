import datetime
import random
from django.conf import settings
from django.shortcuts import render
from app.models import Location, Question
# from django.contrib.auth.decorators import login_required

def _generate_building_question():
    # Seed random number generator with date
    a = datetime.datetime.now() + datetime.timedelta(days=1)
    b = a.strftime("%Y%m%d" + settings.SECRET_KEY)  # add django seed
    random.seed(b)

    # Select todays random question
    pks = Question.objects.values_list('pk', flat=True)
    random_pk = random.choice(pks)
    random_question = Question.objects.get(pk=random_pk)
    return random_question

def _generate_building_location():

    # Seed random number generator with date
    a = datetime.datetime.now() + datetime.timedelta(days=2)
    b = a.strftime("%Y%m%d" + settings.SECRET_KEY)  # add django seed
    random.seed(b)
    # Select todays random location
    pks = Location.objects.values_list('pk', flat=True)
    random_pk = random.choice(pks)
    random_location = Location.objects.get(pk=random_pk)
    return random_location


# @login_required
def home(request):

    daily_location = _generate_building_location()
    daily_question = _generate_building_question()
    context = {
        'building_name': daily_location.name,
        'building_lat': daily_location.latitude,
        'building_lon': daily_location.longitude,
        'building_message': daily_location.location_message,

        'question': daily_question.question,
        'a': daily_question.a,
        'b': daily_question.b,
        'c': daily_question.c,
        'd': daily_question.d,
        #'answer': daily_question.answer,
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
    }
    return render(request, 'app/home.html', context)

# distance check!