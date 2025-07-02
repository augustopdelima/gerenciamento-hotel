from django.contrib import admin

from quartos.models import Quarto, TipoQuarto


@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ["numero", "descricao", "status", "tipo"]
    list_filter = ["tipo", "status"]
    search_fields = ["tipo__nome", "status__tag"]
    ordering = ["numero"]


@admin.register(TipoQuarto)
class TipoQuartoAdmin(admin.ModelAdmin):
    list_display = ["nome", "descricao"]
    list_filter = ["nome", "capacidade"]
    search_fields = ["nome", "capacidade", "descricao"]
