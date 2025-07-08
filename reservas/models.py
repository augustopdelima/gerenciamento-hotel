from django.db import models
from clientes.models import Cliente
from django.contrib.auth.models import User
from quartos.models import Quarto
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


STATUS_RESERVA_CHOICES = [
    ('criada', 'Criada'),
    ('em_andamento', 'Em Andamento'),
    ('finalizada', 'Finalizada'),
    ('cancelada', 'Cancelada'),
]


class Reserva(models.Model):
    data_entrada = models.DateField()
    data_saida = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    funcionario = models.ForeignKey(User, on_delete=models.RESTRICT)
    quarto = models.ForeignKey(Quarto, on_delete=models.RESTRICT)
    criada_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_RESERVA_CHOICES,
        default='criada',
    )

    def __str__(self):
        return f"Reserva #{self.pk} - Cliente: {self.cliente.nome} - Quarto: {self.quarto.numero} - Status:{self.status}"

    def clean(self):

        if self.status in ("cancelada", "finalizada"):
            return

        # verifica datas coerentes
        if self.data_entrada and self.data_saida and self.data_entrada >= self.data_saida:
            raise ValidationError({
                "data_saida": "A data de saída deve ser posterior à data de entrada."
            })

        # quarto não pode estar fora de serviço
        if self.quarto and self.quarto.status in ["manutencao", "indisponivel"]:
            raise ValidationError({
                "quarto": f"O quarto {self.quarto.numero} está {self.quarto.get_status_display().lower()}."
            })

        conflito = (
            Reserva.objects.filter(
                quarto=self.quarto,
                # só essas contam como ativas
                status__in=["criada", "em_andamento"],
                data_entrada__lt=self.data_saida,
                data_saida__gt=self.data_entrada
            )
            .exclude(pk=self.pk)
            .exists()
        )

        if conflito:
            raise ValidationError(
                "Já existe uma reserva para este quarto no período informado."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


@receiver(post_save, sender=Reserva)
def atualiza_status_quarto(sender, instance, **kwargs):
    quarto = instance.quarto

    if instance.status == "criada":
        if quarto.status != "reservado":
            quarto.status = "reservado"
            quarto.save(update_fields=["status"])

    # Reservas que ocupam o quarto
    if instance.status == "em_andamento":
        if quarto.status != "ocupado":
            quarto.status = "ocupado"
            quarto.save(update_fields=["status"])

    # Reservas que liberam o quarto
    elif instance.status in ("finalizada", "cancelada"):
        existe_outra = Reserva.objects.filter(
            quarto=quarto,
            status__in=["criada", "em_andamento"],
            # já iniciadas ou iniciam até a data de saída desta
            data_entrada__lte=instance.data_saida
        ).exclude(pk=instance.pk).exists()

        if not existe_outra:
            quarto.status = "disponivel"
            quarto.save(update_fields=["status"])


class CheckInCheckOut(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.RESTRICT)

    funcionario_checkin = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="checkins_realizados"
    )

    data_checkin = models.DateTimeField()

    funcionario_checkout = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        related_name="checkouts_realizados",
    )

    data_checkout = models.DateTimeField(null=True)

    def __str__(self):
        checkout_str = (
            self.data_checkout.strftime(
                "%d/%m/%Y %H:%M") if self.data_checkout else "—"
        )

        return f'Reserva #{self.reserva.pk} | Check-in: {self.data_checkin.strftime("%d/%m/%Y %H:%M")} | Check-out: {checkout_str}'
