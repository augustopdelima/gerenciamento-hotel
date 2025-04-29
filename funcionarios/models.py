from django.db import models


class Cargo(models.Model):
    nome_funcao = models.CharField(max_length=50)


class Funcionario(models.Model):
    nome = models.CharField(max_length=50)
    ativo = models.BooleanField()
    cpf = models.CharField(max_length=11)
    email = models.CharField(max_length=254)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    def __str__(self):
        return f'Fucionário#{self.id}:{self.nome} - {self.cargo}'
