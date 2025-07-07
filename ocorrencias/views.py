from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Ocorrencia
from .forms import OcorrenciaForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


@login_required
def registrar_ocorrencia(request):
    if request.method == "POST":
        form = OcorrenciaForm(request.POST)
        if form.is_valid():
            ocorrencia = form.save(commit=False)
            ocorrencia.criado_por = request.user
            ocorrencia.save()  # sinais tratam status do quarto

            notificar_manutencao(ocorrencia)
            messages.success(request, "Ocorrência registrada com sucesso.")
            return redirect("lista_ocorrencias")

    else:
        form = OcorrenciaForm()

    return render(request, "ocorrencias/registrar.html", {"form": form})


@login_required
def lista_ocorrencias(request):
    ocorrencias = Ocorrencia.objects.all().order_by('-data_registro')
    return render(request, 'ocorrencias/lista.html', {'ocorrencias': ocorrencias})


@login_required
def marcar_ocorrencia_resolvida(request, ocorrencia_id):
    ocorrencia = get_object_or_404(
        Ocorrencia, pk=ocorrencia_id, resolvido=False)
    ocorrencia.marcar_resolvida()
    messages.success(request, "Ocorrência marcada como resolvida.")
    return redirect("lista_ocorrencias")


@login_required
def excluir_ocorrencia(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, pk=ocorrencia_id)
    ocorrencia.delete()  # sinal post_delete cuida do quarto
    messages.success(request, "Ocorrência excluída com sucesso.")
    return redirect("lista_ocorrencias")


@login_required
def editar_ocorrencia(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, pk=ocorrencia_id)

    if request.method == "POST":
        form = OcorrenciaForm(request.POST, instance=ocorrencia)
        if form.is_valid():
            form.save()
            messages.success(request, "Ocorrência atualizada.")
            return redirect("lista_ocorrencias")
        messages.error(request, "Corrija os erros no formulário.")
    else:
        form = OcorrenciaForm(instance=ocorrencia)

    return render(
        request,
        "ocorrencias/editar_ocorrencia.html",
        {"form": form, "ocorrencia": ocorrencia},
    )


def notificar_manutencao(ocorrencia):
    assunto = "Nova ocorrência!"
    mensagem = (
        f"Uma nova ocorrência foi registrada.\n\n"
        f"Quarto: {ocorrencia.quarto}\n"
        f"Descrição: {ocorrencia.descricao}\n"
        f"Data: {ocorrencia.data_registro}\n"
    )

    try:
        grupo_manutencao = Group.objects.get(name='Manutenção')
        destinatarios = [
            user.email for user in grupo_manutencao.user_set.all() if user.email]
    except Group.DoesNotExist:
        destinatarios = [""]

    send_mail(
        subject=assunto,
        message=mensagem,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=destinatarios,
        fail_silently=False
    )
