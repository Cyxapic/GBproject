from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        verbose_name='Дата рождения'
    )
    avatar = models.ImageField(
        upload_to='accounts/avatar/',
        blank=True,
        null=True,
        verbose_name='Автарка'
    )
    image = models.URLField(
        blank=True,
        null=True,
        verbose_name='G+ автарка'
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = AccountManager()

    def __str__(self):
        return self.email

    @property
    def get_avatar(self):
        if self.avatar:
            avatar = self.avatar.url
        elif self.image:
            avatar = self.image
        else:
            avatar = '/static/accounts/img/anonymous.png'
        return avatar

    @property
    def get_name(self):
        default = 'Ты не указал бро!'
        name = f'{self.last_name} {self.first_name}'
        return name if self.last_name and self.first_name else default

    @property
    def get_birthday(self):
        default = 'А я вот день рождение не буду справлять...!'
        return f'День рождение: {self.birthday}' if self.birthday else default

    def email_user(self, subject, message,
                   from_email=settings.DEFAULT_FROM_EMAIL, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class AccountExtra(models.Model):
    """Proxy Account GB told me to do this :D"""
    OTHER = 'Не Скажу'
    MALE = 'Мужик'
    FEMALE = 'Девушка'
    GENDER = (
        (0, OTHER),
        (1, MALE),
        (2, FEMALE),
    )
    account = models.OneToOneField(
        Account,
        db_index=True,
        on_delete=models.CASCADE
    )
    gender = models.PositiveSmallIntegerField(choices=GENDER, default=0)
    g_plus = models.URLField(
        blank=True,
        null=True,
        verbose_name='G+ link'
    )
    about = models.TextField(
        verbose_name='О себе',
        max_length=512,
        blank=True
    )

    @property
    def get_gender(self):
        gender_tpl = (
            '<i class="fas fa-genderless"></i>',
            '<i class="fas fa-mars"></i>',
            '<i class="fas fa-venus"></i>',
        )
        return gender_tpl[self.gender]

    @property
    def get_g_plus_link(self):
        return self.g_plus if self.g_plus else None

    @receiver(post_save, sender=Account)
    def create_user_extra(sender, instance, created, **kwargs):
        if created:
            AccountExtra.objects.create(account=instance)

    @receiver(post_save, sender=Account)
    def save_user_extra(sender, instance, **kwargs):
        instance.accountextra.save()
