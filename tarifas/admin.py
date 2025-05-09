from django.contrib import admin

from tarifas.models import Tarifa


@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = [
        "valor",
        "tipo_quarto",
        "ativa",
        "data_inicio",
        "data_fim",
        "temporada",
    ]

    search_fields = [
        "tipo_quarto__nome",
        "data_inicio__nome",
    ]

    list_filter = [
        "valor",
        "tipo_quarto",
        "ativa",
        "temporada",
        "data_inicio",
        "data_fim",
    ]

    ordering = ["-data_inicio", "tipo_quarto"]
