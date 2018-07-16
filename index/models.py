from django.db import models


class MainMenu(models.Model):
    url = models.CharField(max_length=30, verbose_name='Имя URL')
    title = models.CharField(max_length=45, verbose_name='Отображаемое имя')
    posnum = models.PositiveSmallIntegerField(verbose_name='Позиция вывод')

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ('posnum',)