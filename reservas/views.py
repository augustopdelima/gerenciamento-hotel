from django.shortcuts import render, redirect
from .models import Reserva
from .forms import ReservaForm
from django.contrib import messages

ORDENACAO_RESERVA_LOOKUP = {
    "cliente": "cliente__nome",
    "data_entrada": "data_entrada",
    "status": "status",
    "data_saida": "data_saida",
}


def reservas(request):
    query = request.GET.get('busca', '')

    if query:
        reservas = Reserva.objects.filter(
            cliente__nome__icontains=query, ativa=True)
    else:
        reservas = Reserva.objects.filter(ativa=True)

    dados = {
        "reservas": reservas,
        "query": query,
        "ativos": True,
    }

    return render(request, 'reservas/index.html', dados)


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
        dados = {
            'form': form,
        }

    return render(request, 'reservas/cadastrar_reserva.html', dados)


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

    dados = {
        'form': form,
        'reserva': reserva,
    }

    return render(request, 'reservas/editar_reserva.html', dados)


def excluir_reserva(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
        reserva.ativa = False
        reserva.save()
        messages.success(request, "Reserva excluída com sucesso.")
    except Reserva.DoesNotExist:
        messages.error(request, "Reserva não encontrado.")

    return redirect("reservas:reservas")


def ordenar_reservas_view(request, campo):
    busca = request.GET.get('busca', '')
    ativo_param = request.GET.get('ativo', 'true').lower()
    ativo = ativo_param == 'true'
    campo_ordenacao = ORDENACAO_RESERVA_LOOKUP[campo]

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


def ativar_reserva(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
    except Reserva.DoesNotExist:
        messages.error(request, "Reserva não encontrado.")
        return redirect('reservas:reservas_inativos')

    if reserva.ativa == False:
        reserva.ativa = True
        reserva.save()
        messages.success(request, "Reserva reativada com sucesso.")

    else:
        messages.info(request, "A reserva já está ativa.")

    return redirect('reservas:reservas_inativas')


def listar_inativas(request):
    query = request.GET.get('busca', '')

    if query:
        reservas = Reserva.objects.filter(
            ativo=False, cliente_nome__icontains=query)
    else:
        reservas = Reserva.objects.filter(ativa=False)

    dados = {
        'reservas': reservas,
        'ativos': False,
        'query': query,
    }

    return render(request, 'reservas/index.html', dados)


def gerar_relatorio_reservas(request):
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    cliente = request.GET.get('cliente', '')
    status = request.GET.get('status', '')
    quarto = request.GET.get('quarto', '')

    reservas = Reserva.objects.all()

    if data_inicio:
        try:
            reservas = reservas.filter(data_entrada__gte=datetime.strptime(data_inicio, '%Y-%m-%d'))
        except ValueError:
            pass 
    if data_fim:
        try:
            reservas = reservas.filter(data_saida__lte=datetime.strptime(data_fim, '%Y-%m-%d'))
        except ValueError:
            pass  
    if cliente:
        reservas = reservas.filter(cliente__nome__icontains=cliente)
    if status:
        reservas = reservas.filter(ativa=(status.lower() == 'ativa'))
    if quarto:
        reservas = reservas.filter(quarto__icontains=quarto)

    dados = {
        'reservas': reservas,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'cliente': cliente,
        'status': status,
        'quarto': quarto,
    }

    return render(request, 'reservas/relatorio_reservas.html', dados)