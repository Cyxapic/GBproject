from django.db import models


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=60)
    text = models.TextField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Статья'
        verbose_name_plural='Статьи'