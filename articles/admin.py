from django.contrib import admin

from .models import Category, Article


admin.site.register(Category)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('title', 'created', 'is_published')
