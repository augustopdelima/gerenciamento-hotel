from django.db import models
from clientes.models import Cliente
from django.contrib.auth.models import User
from quartos.models import Quarto


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

    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"Reserva #{self.pk} - Cliente: {self.cliente.nome} - Quarto: {self.quarto.numero} - Status:{self.status}"


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
