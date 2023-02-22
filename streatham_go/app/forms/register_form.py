from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    template_name = 'app/forms/register_form.html'
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
                                                  'placeholder': 'email',
                                                  'class': 'form-control'}))
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={
                                                  'placeholder': 'Password',
                                                  'class': 'form-control'}))
    rpassword = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Repete Password',
                                    'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        rpassword = cleaned_data.get("rpassword")

        if password != rpassword:
            raise forms.ValidationError(
                "password and repeted password do not match"
            )

        username = cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username allready taken"
            )

        email = cleaned_data.get("email") + '@exeter.ac.uk'

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Username allready taken"
            )
