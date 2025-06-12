from django.contrib import admin

from quartos.models import Quarto, StatusQuarto, TipoQuarto


@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ["numero", "descricao", "status", "tipo"]
    list_filter = ["tipo", "status"]
    search_fields = ["tipo__nome", "status__tag"]
    ordering = ["numero"]


@admin.register(StatusQuarto)
class StatusQuartoAdmin(admin.ModelAdmin):
    list_display = ["tag"]
    list_filter = ["tag"]
    search_fields = ["tag"]


@admin.register(TipoQuarto)
class TipoQuartoAdmin(admin.ModelAdmin):
    list_display = ["nome", "descricao", "capacidade", "quantidade_camas"]
    list_filter = ["nome", "capacidade", "quantidade_camas", "banheiras"]
    search_fields = ["nome", "capacidade", "descricao"]
