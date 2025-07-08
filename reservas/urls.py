from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('cadastrar_reserva/', views.cadastrar_reserva, name='cadastrar_reserva'),
    path('editar_reserva/<int:id>', views.editar_reserva, name='editar_reserva'),
    path('excluir_reserva/<int:id>', views.excluir_reserva, name='excluir_reserva'),
    path('ordenar_reserva/<campo>/',
         views.ordenar_reservas_view, name='ordenar_reserva'),
    path('reservas_inativas/', views.listar_inativas, name="reservas_inativas"),
    path('relatorio/', views.gerar_relatorio_reservas, name='relatorio_reservas'),
    # Check-in
    path("reliazar_checkin/<int:id>",
         views.realizar_checkin, name="realizar_checkin"),
    path("<int:reserva_id>/detalhes/",
         views.detalhes_reserva, name="detalhes_reserva"),
    # Check-out
    path("realizar_checkout/<int:id>",
         views.realizar_checkout, name="realizar_checkout")
]
