from django.urls import path
from . import views

urlpatterns = [
    # Quarto
    path('', views.quartos, name='quartos'),
    path('cadastrar_quarto/', views.cadastrar_quarto,
         name='cadastrar_quarto'),
    path('editar_quarto/<int:id>',
         views.editar_quarto, name='editar_quarto'),
    path('excluir_quarto/<int:id>',
         views.editar_quarto, name='excluir_quarto'),
    path('ordenar/<campo>/', views.ordenar_quartos_view,
         name='ordenar_quarto'),
    # Status
    path('listar_status_quartos/', views.status, name='listar_status_quartos'),
    path('cadastrar_status_quartos/', views.cadastrar_status,
         name='cadastrar_status_quartos'),
    path('editar_status_quartos/<int:id>',
         views.editar_status, name='editar_status_quartos'),
    path('excluir_status_quartos/<int:id>',
         views.excluir_status, name='excluir_status_quartos'),
    path('ordenar_status_quartos/<campo>/', views.ordenar_status_view,
         name='ordenar_status_quartos'),
]
