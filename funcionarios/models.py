from django.db import models


class Cargo(models.Model):
    nome_funcao = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f"{self.nome_funcao}"


class Funcionario(models.Model):
    nome = models.CharField(max_length=50, blank=False)
    ativo = models.BooleanField(default=True)
    email = models.EmailField(max_length=254, blank=False)
    cargo = models.ForeignKey(Cargo, on_delete=models.RESTRICT, blank=False)

    def __str__(self):
        return f"Funcionário#{self.pk}:{self.nome} - {self.cargo}"

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
