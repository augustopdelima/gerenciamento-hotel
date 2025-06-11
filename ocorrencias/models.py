from django.db import models

from quartos.models import Quarto
from funcionarios.models import Funcionario


class Ocorrencia(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.RESTRICT)
    descricao = models.TextField()
    data_registro = models.DateField()
    registrado_por = models.ForeignKey(Funcionario, on_delete=models.RESTRICT)
    resolvido = models.BooleanField(default=False)
    data_resolvido = models.DateTimeField(null=True)

    def __str__(self):
        return f'Ocorrencia#{self.id}:{self.quarto.numero},{self.descricao}'
