from django.shortcuts import render, redirect
from .models import Quarto
from .forms import QuartoForm
from django.contrib import messages
from django.db.models import RestrictedError

ORDENACAO_QUARTOS_LOOKUP = {
    'numero': 'numero',
    'andar': 'andar',
    'descricao': 'descricao',
    'status': 'status__tag',
    'tipo': 'tipo__nome',
}


def quartos(request):
    query = request.GET.get('busca', '')

    if query:
        quartos = Quarto.objects.filter(
            ativo=True, numero__icontains=query)
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

    return render(request, 'quartos/editar_quarto.html', quarto)


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
