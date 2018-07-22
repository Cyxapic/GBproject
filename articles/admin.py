from django.contrib import admin
from django.conf import settings

from .models import Category, Article, ArticleImage


admin.site.register(Category)
admin.site.register(ArticleImage)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('title', 'created', 'is_published', 'updated')
