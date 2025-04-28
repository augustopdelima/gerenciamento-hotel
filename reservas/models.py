from django.db import models
from clientes.models import Cliente
from funcionarios.models import Funcionario


class StatusReserva(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag


class Reserva(models.Model):
    data = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.RESTRICT)
    status = models.ForeignKey(StatusReserva, on_delete=models.RESTRICT)


class CheckInCheckOut(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)

    funcionario_checkin = models.ForeignKey(
        Funcionario, on_delete=models.RESTRICT)

    data_checkin = models.DateTimeField()

    funcionario_checkout = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True)

    data_checkout = models.DateTimeField(null=True)
