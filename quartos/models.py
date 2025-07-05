from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError

QUARTO_STATUS_CHOICES = [
    ("disponivel", "Disponível"),
    ("ocupado", "Ocupado"),
    ("manutencao", "Em Manutenção"),
    ("reservado", "Reservado"),
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

    def clean(self):

        super().clean()

        if not self.pk:
            return

        # Busca o valor que está salvo no banco
        original_status = (
            Quarto.objects.only("status").get(pk=self.pk).status
        )

        # Se o status não mudou
        if original_status == self.status:
            return

        # 3Verifica se há reservas ativas
        Reserva = apps.get_model("reservas", "Reserva")
        reservas_ativas = Reserva.objects.filter(
            quarto=self,
            status__in=["criada", "em_andamento"],
        ).exists()

        if reservas_ativas:
            raise ValidationError(
                {
                    "status":
                        "O status deste quarto é controlado automaticamente "
                        "enquanto houver reservas ativas. "
                        "Para alterar, primeiro finalize ou cancele as reservas ligadas a ele."

                }
            )
