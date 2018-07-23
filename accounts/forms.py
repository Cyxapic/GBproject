from django import forms
from django.contrib.auth import get_user_model
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


class RegForm(forms.ModelForm):
    """Регистрация нового пользователя"""
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

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1',)
        widgets = {
            'username': forms.TextInput(attrs={'autofocus': True,
                                               'class': 'input',
                                               'placeholder': 'Кликуха'}),
        }
        labels = { 'username': 'Кликуха' }


class EditForm(forms.ModelForm):
    """Регистрация нового пользователя"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'last_name', 'first_name', 'birthday', 'avatar')
        widgets = {
            'email': forms.EmailInput(attrs={'autofocus': True,
                                               'class': 'input',
                                               'placeholder': 'Е-МЫЛО'}),
            'last_name': forms.TextInput(attrs={'class': 'input',
                                                'placeholder': 'По паспорту'}),
            'first_name': forms.TextInput(attrs={'class': 'input',
                                                'placeholder': 'Как в паспорте'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'input',
                                               },format = '%Y-%m-%d'),
            'avatar': forms.FileInput(attrs={'class': 'file-input',})
        }
