from django.shortcuts import render, redirect
from .models import Funcionario
from .forms import FuncionarioForm
from django.contrib import messages


def funcionarios(request):
    query = request.GET.get('busca', '')

    if query:
        funcionarios = Funcionario.objects.filter(
            ativo=True, nome__icontains=query)
    else:
        funcionarios = Funcionario.objects.filter(ativo=True)

    dados = {
        'clientes': funcionarios,
        'ativos': True,
        'query': query,
    }

    return render(request, 'funcionarios/index.html', dados)


def funcionarios_excluidos(request):
    query = request.GET.get('busca', '')

    if query:
        funcionarios = Funcionario.objects.filter(
            ativo=False, nome__icontains=query)
    else:
        funcionarios = Funcionario.objects.filter(ativo=False)

    dados = {
        'clientes': funcionarios,
        'ativos': False,
        'query': query,
    }

    return render(request, 'funcionarios/index.html', dados)


def cadastrar_funcionario(request):

    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funcionarios')
    else:
        form = FuncionarioForm()
        dados = {
            'form': form,
        }

    return render(request, 'funcionarios/cadastrar_funcionario.html', dados)


def editar_funcionario(request, id):
    try:
        funcionario = Funcionario.objects.get(id=id)
    except:
        return redirect('clientes')

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('funcionarios')

    form = FuncionarioForm(instance=funcionario)

    dados = {
        'form': form,
        'funcionario': funcionario,
    }

    return render(request, 'funcionarios/editar_funcionarios.html', dados)


def excluir_funcionario(request, id):
    try:
        funcionario = Funcionario.objects.get(id=id)
        funcionario.ativo = False
        funcionario.save()
        messages.success(request, "Funcionário excluído com sucesso.")
    except Funcionario.DoesNotExist:
        messages.error(request, "Funcionário não encontrado.")

    return redirect("funcionarios")


def ativar_funcionario(request, id):
    try:
        funcionario = Funcionario.objects.get(id=id)
    except Funcionario.DoesNotExist:
        messages.error(request, "Funcionario não encontrado.")
        return redirect('funcionario_inativos')

    if funcionario.ativo == False:
        funcionario.ativo = True
        funcionario.save()
        messages.success(request, "Funcionário reativado com sucesso.")

    else:
        messages.info(request, "O funcionário já está ativo.")

    return redirect('funcionario_inativos')


def ordenar_funcionarios_view(request, campo):
    busca = request.GET.get('busca', '')
    ativo_param = request.GET.get('ativo', 'true').lower()
    ativo = ativo_param == 'true'

    funcionarios = Funcionario.objects.filter(ativo=ativo)

    if busca:
        funcionarios = funcionarios.filter(nome__icontains=busca)

    funcionarios = funcionarios.order_by(campo)

    dados = {
        'clientes': funcionarios,
        'ativos': ativo,
        'query': busca,
    }

    return render(request, 'funcionarios/index.html', dados)
