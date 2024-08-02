from django import forms


class UserLoginForm(forms.Form):
    """
        Login user form
    """
    username = forms.CharField(max_length=10,required=True)
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput())
