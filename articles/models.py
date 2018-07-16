import os
from PIL import Image

from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(
            max_length=60,
            verbose_name='Наименование категории')
    description = models.TextField(
            verbose_name='Описание',
            blank=True,
            null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=60)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    thumbnail = models.ImageField(
            upload_to='articles/thumbnails',
            blank=True,
            null=True)
    text = models.TextField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        default = '/static/articles/img/1280x960.png'
        return self.image.url if self.image else default

    @property
    def get_thumbnail(self):
        default = '/static/articles/img/128x128.png'
        return self.thumbnail.url if self.thumbnail else default

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.image:
            SIZE = (128, 128)
            img = Image.open(self.image.path)
            name = f'articles/thumbnails/thum_{self.image.name.split("/")[1]}'
            thumb_path = os.path.join(settings.MEDIA_ROOT, name)
            img.thumbnail(SIZE, Image.ANTIALIAS)
            img.save(thumb_path, 'JPEG', quality=80)
            self.thumbnail = name
            super().save(**kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-created',)
