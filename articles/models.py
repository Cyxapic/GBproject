import os
from PIL import Image

from django.db import models
from django.conf import settings


class Category(models.Model):
    '''Категории статей'''
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
    '''Собственно статьи'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=60)
    text = models.TextField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-created',)


class ArticleImage(models.Model):
    '''Картинки к статьям'''
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    is_title = models.BooleanField(default=False)
    thumbnail = models.ImageField(
            upload_to='articles/thumbnails/',
            blank=True,
            null=True)

    @property
    def get_image(self):
        return self.image.url if self.image else ''

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.image and self.is_title:
            SIZE = (128, 128)
            img = Image.open(self.image.path)
            path = os.path.join(settings.MEDIA_ROOT, 'articles', 'thumbnails')
            if not os.path.exists(path):
                os.mkdir(path)
            name = f'thum_{self.image.name.split("/")[1]}'
            thumb_path = os.path.join(path, name)
            img.thumbnail(SIZE, Image.ANTIALIAS)
            img.save(thumb_path, 'JPEG', quality=80)
            self.thumbnail = f'articles/thumbnails/{name}'
            super().save(**kwargs)
