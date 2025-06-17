from django.urls import path
from . import views

urlpatterns = [
    path('', views.quartos, name='quartos'),
    path('cadastrar_quarto/', views.cadastrar_quarto,
         name='cadastrar_quarto'),
    path('editar_quarto/<int:id>',
         views.editar_quarto, name='editar_quarto'),
    path('excluir_quarto/<int:id>',
         views.editar_quarto, name='excluir_quarto'),
    path('ordenar/<campo>/', views.ordenar_quartos_view,
         name='ordenar_quarto'),
]
