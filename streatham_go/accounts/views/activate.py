from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

from ..tokens import email_verification_token


def activate(request, user_id):
    context = {}
    try:
        uid = force_str(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=uid)
    except (ValueError, DjangoUnicodeDecodeError):
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

            context["success"] = True
        else:
            context["invalid_token"] = True
    return render(request, 'accounts/activate.html', context)
