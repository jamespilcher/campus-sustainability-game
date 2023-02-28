from django.shortcuts import render
from django.contrib.auth.models import User

from ..tokens import email_verification_token
from ..decorators import anonymous_required
from app.models import Leaderboard


@anonymous_required
def activate(request, username):
    context = {}
    try:
        user = User.objects.get(username=username)
    except (ValueError, User.DoesNotExist):
        context["user_not_found"] = True
        user = None

    if not context.get("user_not_found"):
        if request.GET.get("token"):
            token = request.GET["token"]
        else:
            token = ""

        if (user is not None and
                email_verification_token.check_token(user, token)):
            user.is_active = True
            user.save()
            leaderboard = Leaderboard.objects.create(user=user)
            leaderboard.save()

            context["success"] = True
        else:
            context["invalid_token"] = True
    return render(request, 'accounts/activate.html', context)
