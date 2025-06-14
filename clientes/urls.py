from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name='clientes'),
    path('cadastrar_cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('editar_cliente/<int:id>', views.editar_cliente, name='editar_cliente'),
    path('excluir_cliente/<int:id>', views.excluir_cliente, name='excluir_cliente'),
    path('inativos/', views.clientes_excluidos, name='clientes_inativos'),
    path('ativar/<int:id>', views.ativar_cliente, name='ativar_cliente'),
    path('ordenar/<campo>/', views.ordenar_clientes_view, name='ordenar_cliente')
]
