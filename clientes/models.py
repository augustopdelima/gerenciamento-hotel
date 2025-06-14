from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=254, blank=False)
    telefone = models.CharField(max_length=11, blank=False)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Cliente:{self.nome},email:{self.email},telefone:{self.telefone}"

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.formatar_nome(self.nome)
        super().save(*args, **kwargs)

    def formatar_nome(self, nome):
        partes = nome.lower().split()
        minusculas = ['da', 'de', 'do', 'das', 'dos', 'e']

        return ' '.join([
            p if p in minusculas else p.capitalize()
            for p in partes
        ])
