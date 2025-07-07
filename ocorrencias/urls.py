from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ocorrencias, name='lista_ocorrencias'),
    path('ocorrencias/nova/', views.registrar_ocorrencia,
         name='registrar_ocorrencia'),
    path('ocorrencias/<int:ocorrencia_id>/resolver/',
         views.marcar_ocorrencia_resolvida, name='marcar_ocorrencia_resolvida'),
    path("ocorrencias/<int:ocorrencia_id>/desmarcar/",
         views.desmarcar_ocorrencia_resolvida, name="desmarcar_ocorrencia"),
    path('ocorrencias/<int:ocorrencia_id>/excluir/',
         views.excluir_ocorrencia, name='excluir_ocorrencia'),
    path('editar_ocorrencia/<int:ocorrencia_id>/',
         views.editar_ocorrencia, name='editar_ocorrencia'),
]
