from django.db import models
from quartos.models import TipoQuarto
from django.core.exceptions import ValidationError

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

    def clean(self):
        # data_inicio <= data_fim
        if self.data_inicio > self.data_fim:
            raise ValidationError(
                "A data de início deve ser anterior ou igual à data de fim.")

        # valor positivo
        if self.valor <= 0:
            raise ValidationError("O valor da tarifa deve ser positivo.")

        # verifica sobreposição de período
        conflito = Tarifa.objects.filter(
            tipo_quarto=self.tipo_quarto,
            temporada=self.temporada,
            ativa=True,
        ).exclude(pk=self.pk).filter(
            data_inicio__lte=self.data_fim,
            data_fim__gte=self.data_inicio,
        ).exists()

        if conflito:
            raise ValidationError(
                "Já existe uma tarifa ativa para este tipo de quarto, temporada e período que conflita.")

    def save(self, *args, **kwargs):
        self.full_clean()  # chama validações antes de salvar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tarifa para {self.tipo_quarto.nome} ({self.data_inicio} - {self.data_fim})"
