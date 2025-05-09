from django.db import models


class TipoQuarto(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nome}"


class StatusQuarto(models.Model):
    tag = models.CharField(max_length=25, verbose_name="Status do Quarto")

    def __str__(self):
        return f"{self.tag}"


class Quarto(models.Model):
    numero = models.IntegerField(unique=True, verbose_name="Número do Quarto")
    capacidade = models.IntegerField(verbose_name="Capacidade")
    status = models.ForeignKey(
        StatusQuarto, on_delete=models.RESTRICT, verbose_name="Status"
    )
    tipo = models.ForeignKey(
        TipoQuarto, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de Quarto"
    )

    def __str__(self):
        return f"Quarto {self.numero}"
