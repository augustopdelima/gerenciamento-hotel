from django.db import models
from quartos.models import TipoQuarto


TEMPORADA_CHOICES = [
    ('Baixa', 'Baixa Temporada'),
    ('Média', 'Média Temporada'),
    ('Alta', 'Alta Temporada'),
]


class Tarifa(models.Model):
    tipo_quarto = models.ForeignKey(TipoQuarto, on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    temporada = models.CharField(
        max_length=10, choices=TEMPORADA_CHOICES, null=True, blank=True)
    ativa = models.BooleanField(default=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return f"Tarifa para {self.tipo_quarto.nome} ({self.data_inicio} - {self.data_fim})"
