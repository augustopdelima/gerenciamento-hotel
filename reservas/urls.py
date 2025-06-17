from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('cadastrar_reserva/', views.cadastrar_reserva, name='cadastrar_reserva'),
]
