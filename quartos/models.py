from django.db import models


class TipoQuarto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(max_length=400, blank=True, null=True)
    capacidade = models.IntegerField(verbose_name="Capacidade")
    possui_varanda = models.BooleanField(
        default=False, verbose_name="Possui Varanda")
    banheiras = models.BooleanField(
        default=False, verbose_name="Banheiras", help_text="Tem banheiras")
    quantidade_camas = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.nome} - {self.descricao} - {self.capacidade}"


class StatusQuarto(models.Model):
    tag = models.CharField(max_length=25, verbose_name="Status do Quarto")
    descricao = models.TextField(max_length=256, null=True)

    def __str__(self):
        return f"{self.tag}"


class Quarto(models.Model):
    numero = models.IntegerField(unique=True, verbose_name="Número do Quarto")
    andar = models.IntegerField(null=True, blank=True, verbose_name="Andar")
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição")
    status = models.ForeignKey(
        StatusQuarto, on_delete=models.RESTRICT, verbose_name="Status"
    )
    tipo = models.ForeignKey(
        TipoQuarto, on_delete=models.RESTRICT, null=True, verbose_name="Tipo de Quarto"
    )

    def __str__(self):
        return f"Quarto {self.numero}"
