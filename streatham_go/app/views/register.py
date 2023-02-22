from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ..forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    context = {}
    error_message = ""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email'] + '@exeter.ac.uk'
            password = form.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            if not user:
                error_message = "Failed to create User"
            else:
                user.first_name = f_name
                user.last_name = l_name
                user.save()
                return redirect('app:login')
    else:
        form = RegisterForm()

    context["error_message"] = error_message
    context['form'] = form

    return render(request, 'app/register.html', context)
