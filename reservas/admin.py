from django.contrib import admin

from reservas.models import Reserva, CheckInCheckOut


@admin.register(CheckInCheckOut)
class CheckInCheckOutAdmin(admin.ModelAdmin):
    list_display = [
        'reserva',
        'funcionario_checkin',
        'funcionario_checkout',
        'data_checkin',
        'data_checkout',
    ]

    list_filter = [
        'data_checkin',
        'data_checkout',
        'reserva'
    ]

    search_fields = [
        'data_checkin',
        'funcionario_checkin__nome',
        'funcionario_checkin__nome',
        'data_checkout'
    ]


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

    ordering = ['-data_entrada', '-data_saida']
