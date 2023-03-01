import datetime
import json
import math
import datetime
import random
from django.conf import settings
from app.models import Location
import app.views.home
from django.http import HttpResponseBadRequest, JsonResponse


def _generate_building_location_placeholder():

    # Seed random number generator with date
    a = datetime.datetime.now() + datetime.timedelta(days=12)
    b = a.strftime("%Y%m%d" + settings.SECRET_KEY)  # add django seed
    random.seed(b)

    # Select todays random location
    pks = Location.objects.values_list('pk', flat=True)
    random_pk = random.choice(pks)
    random_location = Location.objects.get(pk=random_pk)
    return random_location

# Distance formula to calculate the distance between two sets of coordinates
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Function to check if a building and a set of coordinates are within ~50 meters of each other
def is_within_50m(building_lat, building_lon, user_lat, user_lon):
    # Calculate the distance between the building's location and the provided coordinates
    building_dist = distance(building_lat, building_lon, user_lat, user_lon)
    return building_dist <= 0.00075

def check_coords(request):
    # Get the building's location from the database
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            daily_location = _generate_building_location_placeholder()
            building_lat = daily_location.latitude
            building_lon = daily_location.longitude
            data = json.load(request)
            print(data)
            # Get the user's location from the request
            user_coords = data.get('data')
            user_lat = user_coords['lat']
            user_lon = user_coords['lon']
            # Check if the user is within 50 meters of the building
            if is_within_50m(building_lat, building_lon, user_lat, user_lon):
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
    else:
        return HttpResponseBadRequest('Invalid request')
    