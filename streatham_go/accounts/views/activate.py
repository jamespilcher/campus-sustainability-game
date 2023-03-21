import random
from django.shortcuts import render
from django.contrib.auth.models import User

from ..tokens import email_verification_token
from ..decorators import anonymous_required
from app.models import Leaderboard


# add the anonymous required decorator
@anonymous_required
# activate user function
def activate(request, username):
    # initalize the context variable
    context = {}
    # get the user from the database
    try:
        user = User.objects.get(username=username)
    except (ValueError, User.DoesNotExist):
        # if the user is not found, set the error message
        context["user_not_found"] = True
        user = None

    # check if the user is not found
    if not context.get("user_not_found"):
        # get the token from the request
        if request.GET.get("token"):
            token = request.GET["token"]
        else:
            token = ""

        # check if the token is valid
        if (user is not None and
                email_verification_token.check_token(user, token)):
            # activate the user
            user.is_active = True
            # save the user
            user.save()

            # Create a leaderboard entry for the user now they're verified

            # Randomly generate number between 1 and 10.
            profilePictureIndex = random.randint(1, 10)
            leaderboard = Leaderboard.objects.create(
                user=user, profilePictureIndex=profilePictureIndex)
            
            # Save the leaderboard
            leaderboard.save()

            # set the success message
            context["success"] = True
        else:
            # if the token is invalid, set the error message
            context["invalid_token"] = True
    # render the activate page
    return render(request, 'accounts/activate.html', context)
