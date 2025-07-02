from django.db import models


QUARTO_STATUS_CHOICES = [
    ("disponivel", "Disponível"),
    ("ocupado", "Ocupado"),
    ("manutencao", "Em Manutenção"),
    ("indisponivel", "Indisponível"),
]


class TipoQuarto(models.Model):
    nome = models.CharField(max_length=100, unique=True, blank=False)
    descricao = models.TextField(max_length=400, blank=True, null=True)
    capacidade = models.IntegerField(verbose_name="Capacidade", blank=False)

    def __str__(self):
        return f"{self.nome}"


class Quarto(models.Model):
    numero = models.IntegerField(
        unique=True,
        verbose_name="Número do Quarto"
    )
    andar = models.IntegerField(
        verbose_name="Andar do Quarto"
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição do Quarto"
    )
    status = models.CharField(
        choices=QUARTO_STATUS_CHOICES,
        max_length=25,
        blank=False,
        verbose_name="Status Atual"
    )
    tipo = models.ForeignKey(
        TipoQuarto,
        on_delete=models.RESTRICT,
        verbose_name="Tipo de Quarto"
    )

    def __str__(self):
        return f"Quarto {self.numero}"
