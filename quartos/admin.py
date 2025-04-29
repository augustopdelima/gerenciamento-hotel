from django.contrib import admin

from quartos.models import Quarto


@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'capacidade', 'status', 'tipo']
    list_filter = ['tipo', 'capacidade', 'status']
    search_fields = ['tipo__nome', 'status__tag']
