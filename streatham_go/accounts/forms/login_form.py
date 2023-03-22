from django import forms


# login form
class LoginForm(forms.Form):
    # use the login form template
    template_name = 'accounts/forms/login_form.html'
    # set the form fields
    # username filed
    # add custom form control class
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                                  'placeholder': 'username',
                                                  'class': 'form-control'}))
    # password field
    # add custom form control class
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={
                                                  'placeholder': 'password',
                                                  'class': 'form-control'}))
