from django.contrib import admin

from ocorrencias.models import Ocorrencia


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'quarto__numero',
                    'data_registro', 'registrado_por__username', 'resolvido']
    list_filter = ['resolvido', 'data_registro', 'quarto__numero']
    search_fields = ['descricao', 'quarto__numero', 'registrado_por__username']
    ordering = ['-data_registro']
