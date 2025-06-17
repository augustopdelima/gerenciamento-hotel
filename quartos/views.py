from django.shortcuts import render, redirect
from .models import Quarto, StatusQuarto, TipoQuarto
from .forms import QuartoForm, TipoQuartoForm, StatusQuartoForm
from django.contrib import messages
from django.db.models import RestrictedError

ORDENACAO_QUARTOS_LOOKUP = {
    'numero': 'numero',
    'andar': 'andar',
    'descricao': 'descricao',
    'status': 'status__tag',
    'tipo': 'tipo__nome',
}

ORDENACAO_STATUS_LOOKUP = {
    'tag': 'tag',
    'descricao': 'descricao',
}

# Quarto


def quartos(request):
    query = request.GET.get('busca', '')

    if query:
        quartos = Quarto.objects.filter(numero__icontains=query)
    else:
        quartos = Quarto.objects.all()

    dados = {
        'quartos': quartos,
        'query': query,
    }

    return render(request, 'quartos/index.html', dados)


def cadastrar_quarto(request):

    if request.method == 'POST':
        form = QuartoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quartos')
        else:
            print(form.errors)
    else:
        form = QuartoForm()
        dados = {
            'form': form,
        }

    return render(request, 'quartos/cadastrar_quarto.html', dados)


def editar_quarto(request, id):
    try:
        quarto = Quarto.objects.get(id=id)
    except:
        return redirect('quartos')

    if request.method == 'POST':
        form = QuartoForm(request.POST, instance=quarto)
        if form.is_valid():
            form.save()
            return redirect('quartos')

    form = QuartoForm(instance=quarto)

    dados = {
        'form': form,
        'quarto': quarto,
    }

    return render(request, 'quartos/editar_quarto.html', dados)


def excluir_quarto(request, id):
    try:
        quarto = Quarto.objects.get(id=id)
        quarto.delete()
        messages.success(request, "Quarto excluído com sucesso.")
    except RestrictedError:
        messages.error(
            request, "Não é possível deletar o quarto pois há reservas vinculados.")
    except Quarto.DoesNotExist:
        messages.error(request, "Quarto não encontrado.")

    return redirect("quartos")


def ordenar_quartos_view(request, campo):
    campo_ordenacao = ORDENACAO_QUARTOS_LOOKUP(campo)
    busca = request.GET.get('busca', '')

    quartos = Quarto.objects.all()

    if busca:
        quartos = quartos.filter(numero__icontains=busca)

    quartos = quartos.order_by(campo_ordenacao)

    dados = {
        'quartos': quartos,
        'query': busca,
    }

    return render(request, 'quartos/index.html', dados)

# Status


def status(request):
    query = request.GET.get('busca', '')

    if query:
        status = StatusQuarto.objects.filter(tag__icontains=query)
    else:
        status = StatusQuarto.objects.all()

    dados = {
        'status': status,
        'query': query,
    }

    return render(request, 'quartos/listar_status.html', dados)


def cadastrar_status(request):

    if request.method == 'POST':
        form = StatusQuartoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_status_quartos')
        else:
            print(form.errors)
    else:
        form = StatusQuartoForm()
        dados = {
            'form': form,
        }

    return render(request, 'quartos/cadastrar_status.html', dados)


def editar_status(request, id):
    try:
        stats = StatusQuarto.objects.get(id=id)
    except:
        return redirect('listar_status_quartos')

    if request.method == 'POST':
        form = StatusQuartoForm(request.POST, instance=stats)
        if form.is_valid():
            form.save()
            return redirect('listar_status_quartos')

    form = StatusQuartoForm(instance=stats)

    dados = {
        'form': form,
        'statusquarto': stats,
    }

    return render(request, 'quartos/editar_status.html', dados)


def excluir_status(request, id):
    try:
        stats = StatusQuarto.objects.get(id=id)
        stats.delete()
        messages.success(request, "Status excluído com sucesso.")
    except RestrictedError:
        messages.error(
            request, "Não é possível deletar o status pois há vinculados.")
    except StatusQuarto.DoesNotExist:
        messages.error(request, "Status não encontrado.")

    return redirect("listar_status_quartos")


def ordenar_status_view(request, campo):
    campo_ordenacao = ORDENACAO_STATUS_LOOKUP(campo)
    busca = request.GET.get('busca', '')

    status = StatusQuarto.objects.all()

    if busca:
        status = status.filter(tag__icontains=busca)

    status = status.order_by(campo_ordenacao)

    dados = {
        'status': status,
        'query': busca,
    }

    return render(request, 'quartos/listar_status.html', dados)
