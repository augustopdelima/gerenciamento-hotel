from tarifas.models import Tarifa
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Reserva, CheckInCheckOut, STATUS_RESERVA_CHOICES
from .forms import ReservaForm, RelatorioReservas, CheckInOutFormSet

STATUS_MAP = dict(STATUS_RESERVA_CHOICES)
ORDENACAO_RESERVA_LOOKUP = {
    "cliente": "cliente__nome",
    "data_entrada": "data_entrada",
    "status": "status",
    "data_saida": "data_saida",
}


@login_required
def reservas(request):
    query = request.GET.get('busca', '')

    if query:
        reservas = Reserva.objects.filter(
            cliente__nome__icontains=query, status__in=[
                "criada", "em_andamento", "finalizada"]
        )
    else:
        reservas = Reserva.objects.filter(
            status__in=["criada", "em_andamento", "finalizada"])

    dados = {
        'reservas': reservas,
        'query': query,
        'ativos': True,
    }

    return render(request, 'reservas/index.html', dados)


@login_required
def cadastrar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.funcionario = request.user
            reserva.save()
            messages.success(request, 'Reserva criada com sucesso.')
            return redirect('reservas:reservas')

    else:
        form = ReservaForm()

    return render(request, 'reservas/cadastrar_reserva.html', {'form': form})


@login_required
def editar_reserva(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
    except Reserva.DoesNotExist:
        return redirect('reservas:reservas')

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        formset = CheckInOutFormSet(request.POST, instance=reserva)

        formset_enviado = 'form-TOTAL_FORMS' in request.POST

        form_valido = form.is_valid()
        formset_valido = formset.is_valid() if formset_enviado else True

        if form_valido and formset_valido:
            reserva_editada = form.save(commit=False)

            if 'funcionario' in form.fields:
                reserva_editada.funcionario = form.cleaned_data.get(
                    'funcionario')

            if 'status' in form.fields:
                reserva_editada.status = form.cleaned_data.get('status')

            reserva_editada.save()

            if formset_enviado:
                formset.save()

            if reserva_editada.status in ["criada", "em_andamento", "finalizada"]:
                return redirect('reservas:reservas')
            else:
                return redirect('reservas:reservas_inativas')

        messages.error(
            request, "Erro ao salvar. Verifique os dados do formulário.")

    else:
        form = ReservaForm(instance=reserva)
        formset = CheckInOutFormSet(instance=reserva)

    return render(request, 'reservas/editar_reserva.html', {
        'form': form,
        'formset': formset,
        'reserva': reserva
    })


@login_required
def excluir_reserva(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
        reserva.status = 'cancelada'
        reserva.save()
        messages.success(request, "Reserva excluída com sucesso.")

    except Reserva.DoesNotExist:
        messages.error(request, "Reserva não encontrada.")

    return redirect('reservas:reservas')


@login_required
def ativar_reserva(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
    except Reserva.DoesNotExist:
        messages.error(request, "Reserva não encontrada.")
        return redirect('reservas:reservas_inativas')

    if reserva.status == 'cancelada':
        reserva.status = 'criada'
        reserva.save()
        messages.success(request, "Reserva reativada com sucesso.")
    else:
        messages.info(request, "A reserva já está ativa.")

    return redirect('reservas:reservas_inativas')


@login_required
def listar_inativas(request):

    query = request.GET.get('busca', '')

    filtro = Reserva.objects.filter(status='cancelada')
    if query:
        filtro = filtro.filter(cliente__nome__icontains=query)

    return render(request, 'reservas/index.html', {'reservas': filtro, 'ativos': False, 'query': query})


@login_required
def ordenar_reservas_view(request, campo):

    busca = request.GET.get('busca', '')
    ativo_param = request.GET.get('ativo', 'true').lower()
    ativo = ativo_param == 'true'

    if ativo:
        reservas = Reserva.objects.filter(
            status__in=['criada', 'em_andamento', 'finalizada'])
    else:
        reservas = Reserva.objects.filter(
            status__in=['cancelada'])

    if busca:
        reservas = reservas.filter(cliente__nome__icontains=busca)

    campo_ordenacao = ORDENACAO_RESERVA_LOOKUP.get(campo, 'id')
    reservas = reservas.order_by(campo_ordenacao)

    dados = {
        'reservas': reservas,
        'ativos': ativo,
        'query': busca,
    }
    return render(request, 'reservas/index.html', dados)


@login_required
def gerar_relatorio_reservas(request):

    form = RelatorioReservas(request.GET or None)
    reservas = Reserva.objects.select_related(
        'cliente', 'quarto', 'funcionario').all()

    if form.is_valid():
        data_inicio = form.cleaned_data.get('data_inicio')
        data_fim = form.cleaned_data.get('data_fim')
        cliente = form.cleaned_data.get('cliente')
        status = form.cleaned_data.get('status')
        quarto = form.cleaned_data.get('quarto')

        if data_inicio:
            reservas = reservas.filter(data_entrada__gte=data_inicio)
        if data_fim:
            reservas = reservas.filter(data_saida__lte=data_fim)
        if cliente:
            reservas = reservas.filter(cliente__nome__icontains=cliente)
        if status:
            reservas = reservas.filter(status=status)
        if quarto:
            reservas = reservas.filter(quarto__tipo__nome__icontains=quarto)
    else:
        messages.error(request, form.errors.as_text())

    for reserva in reservas:
        reserva.nome_status = STATUS_MAP.get(
            reserva.status, 'Desconhecido')

    context = {
        'form': form,
        'reservas': reservas,
    }
    return render(request, 'reservas/relatorio_reservas.html', context)


@login_required
def detalhes_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva.objects.select_related(
        "quarto__tipo", "cliente", "funcionario"), pk=reserva_id)

    tarifas = (
        Tarifa.objects
        .filter(
            tipo_quarto=reserva.quarto.tipo,
            ativa=True,
            data_inicio__lte=reserva.data_entrada,
            data_fim__gte=reserva.data_saida,
        )
        .order_by("-data_inicio")
    )

    checkin = getattr(reserva, "checkincheckout", None)

    context = {
        "reserva": reserva,
        "tarifas": tarifas,
        "check": checkin,
    }
    return render(request, "reservas/detalhes.html", context)


# CheckIn

@login_required
def realizar_checkin(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
    except Reserva.DoesNotExist:
        messages.error(request, "Reserva não encontrada.")
        return redirect("reservas:reservas")

    if reserva.status != "criada":
        messages.error(
            request, "Esta reserva não está disponível para check-in.")
        return redirect("reservas:reservas")

    if request.method == "POST":

        CheckInCheckOut.objects.create(
            reserva=reserva,
            funcionario_checkin=request.user,
            data_checkin=timezone.now()
        )

        # Atualiza status da reserva (sinal cuidará do quarto)
        reserva.status = "em_andamento"
        reserva.save()

        messages.success(request, "Check-in realizado com sucesso.")
        return redirect("reservas:reservas")

    return render(request, "reservas/realizar_checkin.html", {
        "reserva": reserva
    })


@login_required
def realizar_checkout(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
    except Reserva.DoesNotExist:
        messages.error(request, "Reserva não encontrada.")
        return redirect("reservas:reservas")

    if reserva.status != "em_andamento":
        messages.error(request, "A reserva não está em andamento.")
        return redirect("reservas:reservas")

    try:
        checkin_checkout = CheckInCheckOut.objects.get(reserva=reserva)
    except CheckInCheckOut.DoesNotExist:
        messages.ERROR(request, "Não existe check in para está reserva")
        return redirect("reservas:reservas")

    if request.method == "POST":
        checkin_checkout.funcionario_checkout = request.user
        checkin_checkout.data_checkout = timezone.now()
        checkin_checkout.save()

        reserva.status = "finalizada"
        reserva.save()

        messages.success(request, "Check-out realizado com sucesso.")
        return redirect("reservas:reservas")

    return render(request, "reservas/realizar_checkout.html", {
        "reserva": reserva,
        "checkin": checkin_checkout
    })
