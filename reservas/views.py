from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import Reserva
from .forms import ReservaForm

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
            cliente__nome__icontains=query, ativa=True
        )
    else:
        reservas = Reserva.objects.filter(ativa=True)

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
            form.save()
            return redirect('reservas:reservas')
        else:
            print(form.errors)
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
        if form.is_valid():
            reserva_editada = form.save()
            if reserva_editada.ativa:
                return redirect('reservas:reservas')
            else:
                return redirect('reservas:reservas_inativas')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'reservas/editar_reserva.html', {'form': form, 'reserva': reserva})

@login_required
def excluir_reserva(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
        reserva.ativa = False
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

    if not reserva.ativa:
        reserva.ativa = True
        reserva.save()
        messages.success(request, "Reserva reativada com sucesso.")
    else:
        messages.info(request, "A reserva já está ativa.")

    return redirect('reservas:reservas_inativas')

@login_required
def listar_inativas(request):
    query = request.GET.get('busca', '')

    if query:
        reservas = Reserva.objects.filter(
            ativa=False, cliente__nome__icontains=query
        )
    else:
        reservas = Reserva.objects.filter(ativa=False)

    return render(request, 'reservas/index.html', {'reservas': reservas, 'ativos': False, 'query': query})

@login_required
def ordenar_reservas_view(request, campo):
    busca = request.GET.get('busca', '')
    ativo_param = request.GET.get('ativo', 'true').lower()
    ativo = ativo_param == 'true'
    campo_ordenacao = ORDENACAO_RESERVA_LOOKUP.get(campo, 'id')

    reservas = Reserva.objects.filter(ativa=ativo)
    if busca:
        reservas = reservas.filter(cliente__nome__icontains=busca)

    reservas = reservas.order_by(campo_ordenacao)

    dados = {
        'reservas': reservas,
        'ativos': ativo,
        'query': busca,
    }
    return render(request, 'reservas/index.html', dados)

@login_required
def gerar_relatorio_reservas(request):
    data_inicio = request.GET.get('data_inicio', '')
    data_fim    = request.GET.get('data_fim', '')
    cliente     = request.GET.get('cliente', '')
    status      = request.GET.get('status', '')
    quarto      = request.GET.get('quarto', '')

    reservas = Reserva.objects.all()

    if data_inicio:
        try:
            dt_ini = datetime.strptime(data_inicio, '%Y-%m-%d')
        except ValueError:
            d, m, y = data_inicio.split('/')
            dt_ini = datetime(int(y), int(m), int(d))
        reservas = reservas.filter(data_entrada__gte=dt_ini)

    if data_fim:
        try:
            dt_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        except ValueError:
            d, m, y = data_fim.split('/')
            dt_fim = datetime(int(y), int(m), int(d))
        reservas = reservas.filter(data_saida__lte=dt_fim)

    if cliente:
        reservas = reservas.filter(cliente__nome__icontains=cliente)

    if status and status.lower() != '':
        ativa_flag = status.lower() == 'ativa'
        reservas = reservas.filter(ativa=ativa_flag)

    if quarto:
        reservas = reservas.filter(quarto__tipo__nome__icontains=quarto)


    context = {
        'reservas': reservas,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'cliente': cliente,
        'status': status,
        'quarto': quarto,
    }
    return render(request, 'reservas/relatorio_reservas.html', context)
