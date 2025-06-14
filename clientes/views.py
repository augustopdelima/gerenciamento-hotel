from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages


def clientes(request):
    query = request.GET.get('busca', '')

    if query:
        clientes = Cliente.objects.filter(ativo=True, nome__icontains=query)
    else:
        clientes = Cliente.objects.filter(ativo=True)

    dados = {
        'clientes': clientes,
        'ativos': True,
        'query': query,
    }

    return render(request, 'clientes/index.html', dados)


def clientes_excluidos(request):
    query = request.GET.get('busca', '')

    if query:
        clientes = Cliente.objects.filter(ativo=False, nome__icontains=query)
    else:
        clientes = Cliente.objects.filter(ativo=False)

    dados = {
        'clientes': clientes,
        'ativos': False,
        'query': query,
    }

    return render(request, 'clientes/index.html', dados)


def cadastrar_cliente(request):

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
        dados = {
            'form': form,
        }

    return render(request, 'clientes/cadastrar_cliente.html', dados)


def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except:
        return redirect('clientes')

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')

    form = ClienteForm(instance=cliente)

    dados = {
        'form': form,
        'cliente': cliente,
    }

    return render(request, 'clientes/editar_cliente.html', dados)


def excluir_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.ativo = False
        cliente.save()
        messages.success(request, "Cliente excluído com sucesso.")
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente não encontrado.")

    return redirect("clientes")


def ativar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente não encontrado.")
        return redirect('clientes_inativos')

    if cliente.ativo == False:
        cliente.ativo = True
        cliente.save()
        messages.success(request, "Cliente reativado com sucesso.")

    else:
        messages.info(request, "O cliente já está ativo.")

    return redirect('clientes_inativos')


def ordenar_clientes_view(request, campo):
    busca = request.GET.get('busca', '')
    ativo_param = request.GET.get('ativo', 'true').lower()
    ativo = ativo_param == 'true'

    clientes = Cliente.objects.filter(ativo=ativo)

    if busca:
        clientes = clientes.filter(nome__icontains=busca)

    clientes = clientes.order_by(campo)

    dados = {
        'clientes': clientes,
        'ativos': ativo,
        'query': busca,
    }

    return render(request, 'clientes/index.html', dados)
