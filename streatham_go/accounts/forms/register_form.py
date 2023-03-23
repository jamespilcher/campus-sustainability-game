from django import forms
from django.contrib.auth.models import User


# register form
class RegisterForm(forms.Form):
    # use register form template
    template_name = 'accounts/forms/register_form.html'
    # store the fields
    # store the first name
    f_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'First Name',
                                                  'class': 'form-control'}))
    # store the last name
    l_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'Last Name',
                                                  'class': 'form-control'}))
    # store the username
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'Username',
                                                  'class': 'form-control'}))
    # store the email
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'Email',
                                                  'class': 'form-control'}))
    # store the password
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={
                                                  'placeholder': 'Password',
                                                  'class': 'form-control'}))
    # store the repeated password
    rpassword = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Repeat Password',
                                    'class': 'form-control'}))

    # custom clean method
    def clean(self):
        # call the super clean method
        cleaned_data = super(RegisterForm, self).clean()

        # get the password and repeated password
        password = cleaned_data.get("password")
        rpassword = cleaned_data.get("rpassword")

        # check if the passwords match
        if password != rpassword:
            # if they don't match, add an error
            self.add_error("rpassword",
                           "password and repeated password do not match!")

        # get the username
        username = cleaned_data.get("username")

        # check if the username is already taken
        if User.objects.filter(username=username).exists():
            # if it is, add an error
            self.add_error('username', "Username already taken!")

        # get the email
        email = cleaned_data.get("email") + '@exeter.ac.uk'

        # check if the email is already taken
        if User.objects.filter(email=email).exists():
            # if it is, add an error
            self.add_error('email', "Email already taken!")
