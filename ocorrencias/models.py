from django.db import models

from quartos.models import Quarto
from funcionarios.models import Funcionario


class Ocorrencia(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_registro = models.DateField()
    registrado_por = models.ForeignKey(Funcionario, on_delete=models.RESTRICT)
    resolvido = models.BooleanField(default=False)
