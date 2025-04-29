from django.contrib import admin

from quartos.models import Quarto, StatusQuarto


@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'capacidade', 'status', 'tipo']
    list_filter = ['tipo', 'capacidade', 'status']
    search_fields = ['tipo__nome', 'status__tag']


@admin.register(StatusQuarto)
class StatusQuartoAdmin(admin.ModelAdmin):
    list_display = ['tag']
    list_filter = ['tag']
    search_fields = ['tag']
