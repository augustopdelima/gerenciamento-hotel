from django.contrib import admin
from .models import Ocorrencia

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'quarto', 'descricao_curta', 'data_registro', 'resolvido', 'data_resolvido')
    list_filter = ('resolvido', 'quarto', 'data_registro')
    search_fields = ('descricao',)

    def descricao_curta(self, obj):
        return obj.descricao[:40] + ('...' if len(obj.descricao) > 40 else '')