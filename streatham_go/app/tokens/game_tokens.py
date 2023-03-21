import jwt
from django.conf import settings
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import DecodeError
from jwt.exceptions import InvalidTokenError


# generate a game token
def generate_game_jwt(user, buldingName):
    # store the user id, building name, and expiration time in the token
    # the expiration time is 10 minutes so a user has 10 minutes with a
    # valid location
    payload = {
        'user_id': user.pk,
        'buildingName': buldingName,
        'exp': datetime.utcnow() + timedelta(minutes=10)
    }
    # create the token, encoded with the secret key and the HS256 algorithm
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    # return the token
    return token


def validate_game_jwt(request, token):
    try:
        # decode the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        # get the user id
        user_id = payload['user_id']
        # get the building name
        buildingName = payload['buildingName']
        # check if the user id in the token matches the user id of the user
        if request.user.pk == user_id:
            # if the user id matches, return the building name
            return buildingName
        # if the user id does not match, return None
    except (ExpiredSignatureError, DecodeError, InvalidTokenError):
        pass
    return None
