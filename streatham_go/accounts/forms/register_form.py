from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    template_name = 'accounts/forms/register_form.html'
    f_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'First Name',
                                                  'class': 'form-control'}))
    l_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'Last Name',
                                                  'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'Username',
                                                  'class': 'form-control'}))
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'Email',
                                                  'class': 'form-control'}))
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={
                                                  'placeholder': 'Password',
                                                  'class': 'form-control'}))
    rpassword = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Repeat Password',
                                    'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        rpassword = cleaned_data.get("rpassword")

        if password != rpassword:
            self.add_error("rpassword",
                           "password and repeated password do not match!")

        username = cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            self.add_error('username', "Username already taken!")

        email = cleaned_data.get("email") + '@exeter.ac.uk'

        if User.objects.filter(email=email).exists():
            self.add_error('email', "Email already taken!")
