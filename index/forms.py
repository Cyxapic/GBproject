from django import forms
from django.contrib.auth.forms import (AuthenticationForm,
                                       UsernameField,
                                       UserCreationForm)


class LoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'class': 'input',
                                      'placeholder': 'Кликуха'}),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "input",
                                          "placeholder": "Пароль"}),
    )


class RegForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "input",
                                          "placeholder": "Пароль"}),
    )
    password2 = forms.CharField(
        label="Сможешь повторить?",
        widget=forms.PasswordInput(attrs={"class": "input",
                                          "placeholder": "Пароль"}),
        strip=False,
    )
    class Meta(UserCreationForm.Meta):
        widgets = {
            'username': forms.TextInput(attrs={'autofocus': True,
                                               'class': 'input',
                                               'placeholder': 'Кликуха'}),
        }
        labels = {
            'username': 'Кликуха'
        }
