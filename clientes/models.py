from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    telefone = models.CharField(max_length=11)
