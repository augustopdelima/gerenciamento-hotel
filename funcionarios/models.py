from django.db import models


class Cargo(models.Model):
    nome_funcao = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome_funcao}"


class Funcionario(models.Model):
    nome = models.CharField(max_length=50)
    ativo = models.BooleanField()
    cpf = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=254)
    cargo = models.ForeignKey(Cargo, on_delete=models.RESTRICT)

    def __str__(self):
        return f"Funcionário#{self.pk}:{self.nome} - {self.cargo}"
