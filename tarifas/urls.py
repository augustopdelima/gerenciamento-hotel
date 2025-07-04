from django.urls import path
from . import views

urlpatterns = [
    path('tarifas/', views.lista_tarifas, name='lista_tarifas'),
    path('tarifas/nova/', views.nova_tarifa, name='nova_tarifa'),
    path('tarifas/<int:tarifa_id>/editar/', views.editar_tarifa, name='editar_tarifa'),
]
