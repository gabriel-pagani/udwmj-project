from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput()
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already in use.')
        return username
