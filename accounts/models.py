from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя
        auth field email
    """
    email = models.EmailField(unique=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True)
    first_name = models.CharField('Имя', max_length=50, blank=True)
    birthday = models.DateField(
            blank=True,
            null=True,
            verbose_name='Дата рождения')
    avatar = models.ImageField(
            upload_to='accounts/avatar/',
            blank=True,
            null=True,
            verbose_name='Автарка')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = AccountManager()

    def __str__(self):
        return self.email

    @property
    def get_avatar(self):
        default = '/static/accounts/img/anonymous.png'
        return self.avatar.url if self.avatar else default

    @property
    def get_name(self):
        default = 'Ты не указал бро!'
        name = f'{self.last_name} {self.first_name}'
        return name if self.last_name and self.first_name else default

    @property
    def get_birthday(self):
        default = 'А я вот день рождение не буду справлять...!'
        return self.birthday if self.birthday else default

    def email_user(self, subject, message,
                   from_email=settings.DEFAULT_FROM_EMAIL, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
