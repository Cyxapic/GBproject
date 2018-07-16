from django.contrib import admin

from .models import MainMenu


@admin.register(MainMenu)
class MainMenuAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'posnum')