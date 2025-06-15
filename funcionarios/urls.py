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
    path('cargos/', views.cargos, name='cargos'),
    path('cadastrar_cargo', views.cadastrar_cargo, name='cadastrar_cargo'),
    path('editar_cargo/<int:id>', views.editar_cargo, name='editar_cargo'),
    path('excluir_cargo/<int:id>', views.excluir_cargo, name='excluir_cargo'),
    path('ordenar_cargo/<campo>/', views.ordenar_cargos_view, name='ordenar_cargo'),
]
