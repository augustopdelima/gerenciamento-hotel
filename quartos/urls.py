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
         views.excluir_quarto, name='excluir_quarto'),
    path('ordenar/<campo>/', views.ordenar_quartos_view,
         name='ordenar_quarto'),
    # Tipos
    path('tipos_quarto/', views.tipos, name='tipos_quarto'),
    path('cadastrar_tipo/', views.cadastrar_tipo, name='cadastrar_tipo'),
    path('editar_tipo/<int:id>', views.editar_tipo, name='editar_tipo'),
    path('excluir_tipo/<int:id>', views.excluir_tipo, name='excluir_tipo'),
    path('ordernar_tipo/<campo>/', views.ordenar_tipos_view, name='ordenar_tipo')
]
