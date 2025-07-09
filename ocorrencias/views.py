from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Ocorrencia
from .forms import OcorrenciaForm, RelatorioOcorrencias
from django.shortcuts import get_object_or_404
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
    form = RelatorioOcorrencias(request.GET or None)
    ocorrencias = Ocorrencia.objects.select_related(
        'quarto', 'criado_por').all()

    if form.is_valid():
        cd = form.cleaned_data

        if cd['data_inicio']:
            ocorrencias = ocorrencias.filter(
                data_registro__gte=cd['data_inicio'])
        if cd['data_fim']:
            ocorrencias = ocorrencias.filter(data_registro__lte=cd['data_fim'])
        if cd['quarto']:
            ocorrencias = ocorrencias.filter(quarto=cd['quarto'])

        if cd['resolvido'] == 'sim':
            ocorrencias = ocorrencias.filter(resolvido=True)
        elif cd['resolvido'] == 'nao':
            ocorrencias = ocorrencias.filter(resolvido=False)

        if cd['criado_por']:
            ocorrencias = ocorrencias.filter(
                criado_por__username__icontains=cd['criado_por'])

    context = {
        'form': form,
        'ocorrencias': ocorrencias,
    }
    return render(request, 'ocorrencias/lista.html', context)


@login_required
def marcar_ocorrencia_resolvida(request, ocorrencia_id):
    ocorrencia = get_object_or_404(
        Ocorrencia, pk=ocorrencia_id, resolvido=False)
    ocorrencia.marcar_resolvida()
    messages.success(request, "Ocorrência marcada como resolvida.")
    return redirect("lista_ocorrencias")


@login_required
def desmarcar_ocorrencia_resolvida(request, ocorrencia_id):
    ocorrencia = get_object_or_404(
        Ocorrencia, pk=ocorrencia_id, resolvido=True)
    ocorrencia.resolvido = False
    ocorrencia.data_resolvido = None
    ocorrencia.save()
    messages.info(request, "Ocorrência marcada como pendente novamente.")
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
