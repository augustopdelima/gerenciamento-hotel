from django.contrib import admin

from ocorrencias.models import Ocorrencia


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ["descricao"]
