from django.db import models
from clientes.models import Cliente
from funcionarios.models import Funcionario
from quartos.models import Quarto


class StatusReserva(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.tag}"


class Reserva(models.Model):
    data_entrada = models.DateField()
    data_saida = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.RESTRICT)
    status = models.ForeignKey(StatusReserva, on_delete=models.RESTRICT)
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva #{self.pk} - Cliente: {self.cliente.nome} - Quarto: {self.quarto.numero}"


class CheckInCheckOut(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)

    funcionario_checkin = models.ForeignKey(
        Funcionario, on_delete=models.RESTRICT, related_name="checkins_realizados"
    )

    data_checkin = models.DateTimeField()

    funcionario_checkout = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
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
