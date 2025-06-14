from django.urls import path
from . import views

urlpatterns = [
    path('', views.funcionarios, name='funcionarios'),
    path('cadastrar_funcionario/', views.cadastrar_funcionario,
         name='cadastrar_funcionario'),
    path('editar_funcionario/<int:id>',
         views.editar_funcionario, name='editar_funcionario'),
    path('excluir_funcionario/<int:id>',
         views.excluir_funcionario, name='excluir_funcionario'),
    path('inativos/', views.funcionarios_excluidos, name='funcionarios_inativos'),
    path('ativar/<int:id>', views.ativar_funcionario, name='ativar_funcionario'),
    path('ordenar/<campo>/', views.ordenar_funcionarios_view,
         name='ordenar_funcionario'),
]
