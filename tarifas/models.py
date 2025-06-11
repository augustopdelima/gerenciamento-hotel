from django.db import models
from quartos.models import TipoQuarto


class Temporada(models.Model):
    nome = models.CharField(max_length=25)
    
    def __str__(self):
        return f"{self.nome}"


class Tarifa(models.Model):
    tipo_quarto = models.ForeignKey(TipoQuarto, on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    temporada = models.ForeignKey(Temporada, on_delete=models.RESTRICT, null=True)
    ativa = models.BooleanField(default=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return f"Tarifa para {self.tipo_quarto.nome} ({self.data_inicio} - {self.data_fim})"
