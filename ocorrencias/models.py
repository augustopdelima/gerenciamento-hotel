from django.db import models
from quartos.models import Quarto
from django.contrib.auth.models import User

class Ocorrencia(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.RESTRICT)
    descricao = models.TextField()
    data_registro = models.DateField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)
    data_resolvido = models.DateTimeField(null=True, blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f'Ocorrencia#{self.id}:{self.quarto.numero},{self.descricao}'
