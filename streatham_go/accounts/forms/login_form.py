from django import forms


class LoginForm(forms.Form):
    template_name = 'accounts/forms/login_form.html'
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'username',
                                                  'class': 'form-control'}))
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={
                                                  'placeholder': 'password',
                                                  'class': 'form-control'}))
