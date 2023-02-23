from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from urllib.parse import urlencode
from django.utils.http import urlsafe_base64_encode
from ..forms import RegisterForm
from ..decorators import anonymous_required
from ..tokens import email_verification_token
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction


def _send_verification_email(request, user):
    subject = "StreathmGo! Email Verification"
    message = render_to_string(
        'emails/email_verification.html',
        {
            'target_user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_verification_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
    )

    email = EmailMessage(subject,
                         message,
                         to=[user.email],
                         from_email=settings.EMAIL_HOST_USER)

    if email.send():
        return True
    return False


@anonymous_required
@transaction.atomic
def register(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email'] + '@exeter.ac.uk'
            password = form.cleaned_data['password']

            user = User.objects.create_user(username,
                                            email,
                                            password)
            if not user:
                context['error'] = True
            else:
                user.first_name = f_name
                user.last_name = l_name
                user.is_active = False
                if not _send_verification_email(request, user):
                    context['email_error'] = True
                    transaction.set_rollback(True)
                else:
                    user.save()

                    base_redirect_url = reverse('accounts:login')
                    qurey_string = urlencode({'register_success': True})
                    url = '{}?{}'.format(base_redirect_url, qurey_string)
                    return redirect(url)
    else:
        form = RegisterForm()

    context['form'] = form

    return render(request, 'accounts/register.html', context)
