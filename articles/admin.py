from django.contrib import admin
from django.conf import settings

from .models import Category, Article, ArticleImage


admin.site.register(Category)
admin.site.register(ArticleImage)


class ExtendedAdmin(admin.ModelAdmin):
    class Media:
        js = (
            "https://cloud.tinymce.com/stable/tinymce.min.js",
            f"{settings.STATIC_URL}index/js/tinymce_init.js",
        )


@admin.register(Article)
class ArticleAdmin(ExtendedAdmin):
    date_hierarchy = 'created'
    list_display = ('title', 'created', 'is_published', 'updated')

    class Meta:
        wysiwyg_fields = ('text',)
