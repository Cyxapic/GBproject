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

    @property
    def get_email(self):
        default = 'Ты не указал бро!'
        return self.email if self.email else default

    @property
    def get_name(self):
        default = 'Ты не указал бро!'
        name = f'{self.last_name} {self.first_name}'
        return name if self.last_name and self.first_name else default

    @property
    def get_birthday(self):
        default = 'А я вот день рождение не буду справлять...!'
        return self.birthday if self.birthday else default
