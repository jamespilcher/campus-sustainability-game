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


# get activation url private function
def _get_activation_url(request, user):
    # get the protocol
    protocol = 'https' if request.is_secure() else 'http'
    # get the domain
    domain = get_current_site(request).domain
    # get the username
    username = user.username
    # generate the token
    token = email_verification_token.make_token(user)
    # generate the url
    url = "{}://{}/accounts/{}/activate?token={}".format(protocol,
                                                         domain,
                                                         username,
                                                         token)
    # return the url
    return url


# send verification email private function
def _send_verification_email(request, user, url):
    # create the email
    subject = "StreathmGo! Email Verification"
    # render the email template
    html_message = render_to_string(
        'emails/email_verification.html',
        {
            'target_user': user,
            'url': url
        }
    )
    # strip the html tags
    plain_message = strip_tags(html_message)
    # get the from email address
    from_email = settings.EMAIL_HOST_USER
    # get the to email address
    to = user.email

    # send the email
    if send_mail(subject,
                 plain_message,
                 from_email,
                 [to],
                 html_message=html_message,
                 fail_silently=True):
        # if the email is sent, return true
        return True
    # if the email is not sent, return false
    return False


# add the anonymous required decorator
@anonymous_required
# set the transaction to be atomic. This means that if
# any of the queries fail, the database will be rolled
@transaction.atomic
# register view function
def register(request):
    # initalize the context variable
    context = {}
    # check if the request is a post request
    if request.method == 'POST':
        # get the register form
        form = RegisterForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            # get the form data
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email'] + '@exeter.ac.uk'
            password = form.cleaned_data['password']

            # create the user
            user = User.objects.create_user(username,
                                            email,
                                            password)
            # check if the user is not created
            if not user:
                # if the user is not created, set the error message
                context['error'] = True
            else:
                # set the user details
                user.first_name = f_name
                user.last_name = l_name
                user.is_active = False
                # get the activation url
                url = _get_activation_url(request, user)
                # send the verification email
                # if debug is on, save it as a dev activation url
                if (not settings.DEBUG and
                    not _send_verification_email(request,
                                                 user,
                                                 url)):
                    # if the email is not sent, set the error message
                    context['email_error'] = True
                    # set the transaction to be rolled back
                    transaction.set_rollback(True)
                else:
                    # if the email is sent, save the user
                    user.save()

                    # redirect to the login page
                    base_redirect_url = reverse('accounts:login')
                    # if debug is on, add the dev url to the query string
                    query = {'register_success': True}
                    if settings.DEBUG:
                        query['dev_url'] = url

                    # encode the query string
                    qurey_string = urlencode(query)
                    # redirect to the login page with the query string
                    url = '{}?{}'.format(base_redirect_url, qurey_string)
                    # redirect to the login page
                    return redirect(url)
    else:
        # if the request is not a post request, create the register form
        form = RegisterForm()

    # set the context variables
    context['form'] = form

    # render the register page
    return render(request, 'accounts/register.html', context)
