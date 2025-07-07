from django.db import models
from quartos.models import Quarto
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction


class Ocorrencia(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.RESTRICT)
    descricao = models.TextField()
    data_registro = models.DateField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)
    data_resolvido = models.DateTimeField(null=True, blank=True)
    criado_por = models.ForeignKey(
        User, on_delete=models.PROTECT)

    def clean(self):
        super().clean()
        status_quarto = self.quarto.status
        if status_quarto in ['ocupado', 'reservado']:
            raise ValidationError(
                f"Não é possível criar ocorrência para quartos com status '{status_quarto}'."
            )

    def marcar_resolvida(self):

        if not self.resolvido:
            self.resolvido = True
            self.data_resolvido = timezone.now()
            self.save(update_fields=["resolvido", "data_resolvido"])

    def __str__(self):
        return f'Ocorrencia#{self.id}:{self.quarto.numero},{self.descricao}'


@receiver(post_save, sender=Ocorrencia)
def sync_quarto_apos_save(sender, instance, created, **kwargs):
    """
    • Se a ocorrência acabou de ser criada (created=True) e
      o quarto estava 'disponivel'  ➜ muda para 'manutencao'.
    • Sempre que uma ocorrência é marcada como resolvida
      verifica se restam pendentes; se não restarem e o quarto
      está 'manutencao' ➜ volta para 'disponivel'.
    """
    quarto = instance.quarto

    def _atualiza():
        # Se foi criada
        if created and quarto.status in ["disponivel", "manutencao", "indisponivel"]:
            quarto.status = "manutencao"
            quarto.save(update_fields=["status"])

        # Se foi editada para resolvida
        elif instance.resolvido and quarto.status == "manutencao":
            pendentes = Ocorrencia.objects.filter(
                quarto=quarto, resolvido=False).exists()
            if not pendentes:
                quarto.status = "disponivel"
                quarto.save(update_fields=["status"])

    # Garante que o update do quarto rode após o commit da ocorrência
    transaction.on_commit(_atualiza)


@receiver(post_delete, sender=Ocorrencia)
def sync_quarto_apos_delete(sender, instance, **kwargs):
    """
    Se não restarem ocorrências pendentes para o quarto e ele
    estiver em 'manutencao', libera para 'disponivel'.
    """
    quarto = instance.quarto

    def _atualiza():
        pendentes = Ocorrencia.objects.filter(
            quarto=quarto, resolvido=False).exists()
        if not pendentes and quarto.status == "manutencao":
            quarto.status = "disponivel"
            quarto.save(update_fields=["status"])

    transaction.on_commit(_atualiza)
