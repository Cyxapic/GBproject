from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    '''Переопределяем модель пользователя'''
    birthday = models.DateField(blank=True, null=True,
                                verbose_name='Дата рождения')
    avatar = models.ImageField(
            upload_to='accounts/avatar/',
            blank=True,
            verbose_name='Автарка')

    @property
    def get_avatar(self):
        default = '/static/accounts/img/anonymous.png'
        return self.avatar.url if self.avatar else default
