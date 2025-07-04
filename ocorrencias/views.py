from django.shortcuts import render, redirect
from .models import Ocorrencia
from .forms import OcorrenciaForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def registrar_ocorrencia(request):
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST)
        if form.is_valid():
            ocorrencia = form.save(commit=False)
            ocorrencia.criado_por = request.user
            ocorrencia.save()
            notificar_manutencao(ocorrencia)
            return redirect('lista_ocorrencias')
    else:
        form = OcorrenciaForm()
    return render(request, 'ocorrencias/registrar.html', {'form': form})

@login_required
def lista_ocorrencias(request):
    ocorrencias = Ocorrencia.objects.select_related('quarto', 'criado_por').order_by('-data_registro')
    return render(request, 'ocorrencias/lista.html', {'ocorrencias': ocorrencias})

@login_required
def marcar_ocorrencia_resolvida(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
    if not ocorrencia.resolvido:
        ocorrencia.resolvido = True
        ocorrencia.data_resolvido = timezone.now()
        ocorrencia.save()
    return redirect('lista_ocorrencias')

from django.contrib import messages

@login_required
def excluir_ocorrencia(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
    ocorrencia.delete()
    messages.success(request, "Ocorrência excluída com sucesso.")
    return redirect('lista_ocorrencias')


def notificar_manutencao(ocorrencia):
    assunto = f"Nova ocorrência!"
    mensagem = (
        f"Uma nova ocorrência foi registrada.\n\n"
        f"Quarto: {ocorrencia.quarto}\n"
        f"Descrição: {ocorrencia.descricao}\n"
        f"Data: {ocorrencia.data_registro}\n"
    )
    destinatarios = ['juanribeiro@ienh.com.br']

    send_mail(
        assunto,
        mensagem,
        settings.DEFAULT_FROM_EMAIL,
        destinatarios,
        fail_silently=False
    )
