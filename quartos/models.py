from django.db import models


class TipoQuarto(models.Model):
    nome = models.CharField(max_length=100, unique=True, blank=False)
    descricao = models.TextField(max_length=400, blank=True, null=True)
    capacidade = models.IntegerField(verbose_name="Capacidade", blank=False)
    possui_varanda = models.BooleanField(
        default=False, verbose_name="Possui Varanda")
    banheiras = models.BooleanField(
        default=False,  verbose_name="Tem Banheiras",
        help_text="O quarto possui banheiras?")

    def __str__(self):
        return f"{self.nome}"


class StatusQuarto(models.Model):
    tag = models.CharField(
        max_length=25, verbose_name="Status do Quarto", blank=False)
    descricao = models.TextField(
        max_length=256, null=True, blank=True, verbose_name="Descrição")

    def __str__(self):
        return f"{self.tag}"


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
    status = models.ForeignKey(
        StatusQuarto,
        on_delete=models.RESTRICT,
        verbose_name="Status Atual"
    )
    tipo = models.ForeignKey(
        TipoQuarto,
        on_delete=models.RESTRICT,
        verbose_name="Tipo de Quarto"
    )

    def __str__(self):
        return f"Quarto {self.numero}"
