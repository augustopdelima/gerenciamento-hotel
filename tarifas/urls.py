from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tarifas, name='lista_tarifas'),
    path('nova/', views.nova_tarifa, name='nova_tarifa'),
    path('<int:tarifa_id>/editar/',
         views.editar_tarifa, name='editar_tarifa'),
]
