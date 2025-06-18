from django.shortcuts import render, redirect
from .models import Funcionario, Cargo
from .forms import FuncionarioForm, CargoForm
from django.contrib import messages
from django.db.models import RestrictedError

ORDENCAO_FUNCIONARIO_LOOKUP = {
    "nome": "nome",
    "email": "email",
    "cargo": "cargo__nome_funcao"
}

ORDENCAO_CARGO_LOOKUP = {
    "nome_funcao": "nome_funcao"
}


def funcionarios(request):
    query = request.GET.get('busca', '')

    if query:
        funcionarios = Funcionario.objects.filter(
            ativo=True, nome__icontains=query)
    else:
        funcionarios = Funcionario.objects.filter(ativo=True)

    dados = {
        'funcionarios': funcionarios,
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
        'funcionarios': funcionarios,
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
            print(form.errors)
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

    return render(request, 'funcionarios/editar_funcionario.html', dados)


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
        return redirect('funcionarios_inativos')

    if funcionario.ativo == False:
        funcionario.ativo = True
        funcionario.save()
        messages.success(request, "Funcionário reativado com sucesso.")

    else:
        messages.info(request, "O funcionário já está ativo.")

    return redirect('funcionarios_inativos')


def ordenar_funcionarios_view(request, campo):
    busca = request.GET.get('busca', '')
    ativo_param = request.GET.get('ativo', 'true').lower()
    ativo = ativo_param == 'true'
    campo_ordencao = ORDENCAO_FUNCIONARIO_LOOKUP[campo]

    funcionarios = Funcionario.objects.filter(ativo=ativo)

    if busca:
        funcionarios = funcionarios.filter(nome__icontains=busca)

    funcionarios = funcionarios.order_by(campo_ordencao)

    dados = {
        'funcionarios': funcionarios,
        'ativos': ativo,
        'query': busca,
    }

    return render(request, 'funcionarios/index.html', dados)

# Cargo


def cargos(request):
    query = request.GET.get('busca', '')

    if query:
        cargos = Cargo.objects.filter(nome__icontains=query)
    else:
        cargos = Cargo.objects.all()

    dados = {
        'cargos': cargos,
        'query': query,
    }

    return render(request, 'funcionarios/listar_cargos.html', dados)


def cadastrar_cargo(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cargos')
    else:
        form = CargoForm()
        dados = {
            'form': form,
        }

    return render(request, 'funcionarios/cadastrar_cargo.html', dados)


def editar_cargo(request, id):
    try:
        cargo = Cargo.objects.get(id=id)
    except:
        return redirect('cargo')

    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('cargos')

    form = CargoForm(instance=cargo)

    dados = {
        'form': form,
        'cargo': cargo,
    }

    return render(request, 'funcionarios/editar_cargo.html', dados)


def excluir_cargo(request, id):
    try:
        cargo = Cargo.objects.get(id=id)
        cargo.delete()
        messages.success(request, "Cargo excluído com sucesso.")
    except RestrictedError:
        messages.error(
            request, "Não é possível deletar o cargo pois há funcionários vinculados.")
    except Cargo.DoesNotExist:
        messages.error(request, "Cargo não encontrado.")

    return redirect("cargos")


def ordenar_cargos_view(request, campo):
    busca = request.GET.get('busca', '')
    campo_ordenacao = ORDENCAO_CARGO_LOOKUP[campo]

    cargos = Cargo.objects.all()

    if busca:
        cargos = cargos.filter(nome_funcao__icontains=busca)

    cargos = cargos.order_by(campo_ordenacao)

    dados = {
        'cargos': cargos,
        'query': busca,
    }

    return render(request, 'funcionarios/listar_cargos.html', dados)
