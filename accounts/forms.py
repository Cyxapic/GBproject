from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator


class LoginForm(forms.ModelForm):
    email = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'class': 'input',
                                      'placeholder': 'Email'}),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input',
                                          'placeholder': 'Пароль'}),
    )
    remeber = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class':'titul-img'})
    )
    user_cache = None

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Неверный email или пароль!")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Аккаунт не активен!")
        return self.cleaned_data

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


class RegForm(forms.ModelForm):
    """Регистрация нового пользователя"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1',)
        widgets = {
            'email': forms.TextInput(attrs={'autofocus': True,
                                            'class': 'input',
                                            'placeholder': 'Почтовый ящик'}),
        }
        labels = { 'username': 'Кликуха' }

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

    def __init__(self, *args, **kwargs):
        self.domain = kwargs.pop('domain', None)
        super().__init__(*args, **kwargs)

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password1

    def send_activation(self, user):
        token = default_token_generator.make_token(user)
        url = f'{self.domain}/accounts/activate/{user.id}/{token}'
        subject = 'Подтверждение регистрации'
        message = f'''Добрый день {user.email}, спасибо за регистрацию.
                  Для активации Вашего аккаунта необходимо пройти по ссылке
                  {url}'''
        user.email_user(subject, message)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            self.send_activation(user)
        return user


class EditForm(forms.ModelForm):
    """Правка профиля"""
    class Meta:
        model = get_user_model()
        fields = ('last_name', 'first_name', 'birthday', 'avatar')
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'input',
                                                'placeholder': 'По паспорту'}),
            'first_name': forms.TextInput(attrs={'class': 'input',
                                                'placeholder': 'Как в паспорте'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'input',
                                               },format = '%Y-%m-%d'),
            'avatar': forms.FileInput(attrs={'class': 'file-input',})
        }
