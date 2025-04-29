from django.contrib import admin

from reservas.models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = [
        'data_entrada',
        'data_saida',
        'cliente',
        'funcionario',
        'status',
        'quarto',
        'criada_em'
    ]

    list_filter = [
        'funcionario',
        'data_entrada',
        'data_saida',
        'status',
        'cliente',
        'quarto',
        'criada_em'
    ]

    search_fields = [
        'quarto__numero',
        'status__tag',
        'data_entrada',
        'data_saida',
        'funcionario__nome',
        'cliente__nome'
    ]
