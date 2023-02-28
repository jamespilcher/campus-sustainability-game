from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlencode
from ..forms import RegisterForm
from ..decorators import anonymous_required
from ..tokens import email_verification_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.utils.html import strip_tags
from app.models import Leaderboard


def _get_activation_url(request, user):
    protocol = 'https' if request.is_secure() else 'http'
    domain = get_current_site(request).domain
    username = user.username
    token = email_verification_token.make_token(user)
    url = "{}://{}/accounts/{}/activate?token={}".format(protocol,
                                                         domain,
                                                         username,
                                                         token)
    return url


def _send_verification_email(request, user, url):
    subject = "StreathmGo! Email Verification"
    html_message = render_to_string(
        'emails/email_verification.html',
        {
            'target_user': user,
            'url': url
        }
    )
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email

    if send_mail(subject,
                 plain_message,
                 from_email,
                 [to],
                 html_message=html_message,
                 fail_silently=True):
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
                url = _get_activation_url(request, user)
                if (not settings.DEBUG and
                    not _send_verification_email(request,
                                                 user,
                                                 url)):
                    context['email_error'] = True
                    transaction.set_rollback(True)
                else:
                    user.save()
                    leaderboard = Leaderboard.objects.create(user=user)
                    leaderboard.save()

                    base_redirect_url = reverse('accounts:login')
                    query = {'register_success': True}
                    if settings.DEBUG:
                        query['dev_url'] = url

                    qurey_string = urlencode(query)
                    url = '{}?{}'.format(base_redirect_url, qurey_string)
                    return redirect(url)
    else:
        form = RegisterForm()

    context['form'] = form

    return render(request, 'accounts/register.html', context)
