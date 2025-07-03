from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import FuncionarioForm


ORDER_FUNCIONARIO_LOOKUP = {
    "nome": "first_name",
    "email": "email",
    "cargo": "groups__name",
}


@login_required
def funcionarios(request):
    query = request.GET.get('busca', '')

    if query:
        funcionarios = User.objects.filter(
            is_active=True, username__icontains=query)
    else:
        funcionarios = User.objects.filter(is_active=True)

    dados = {
        'funcionarios': funcionarios,
        'ativos': True,
        'query': query,
    }

    return render(request, 'funcionarios/index.html', dados)


@login_required
def funcionarios_excluidos(request):
    query = request.GET.get('busca', '')

    if query:
        funcionarios = User.objects.filter(
            is_active=False, username__icontains=query)
    else:
        funcionarios = User.objects.filter(is_active=False)

    dados = {
        'funcionarios': funcionarios,
        'ativos': False,
        'query': query,
    }

    return render(request, 'funcionarios/index.html', dados)


@login_required
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


@login_required
def editar_funcionario(request, id):
    try:
        funcionario = User.objects.get(pk=id)
    except:
        return redirect('funcionarios')

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário editado!")
            return redirect('funcionarios')
        else:
            messages.error(request, form.error_messages)

    form = FuncionarioForm(instance=funcionario)

    dados = {
        'form': form,
        'funcionario': funcionario,
    }

    return render(request, 'funcionarios/editar_funcionario.html', dados)


@login_required
def excluir_funcionario(request, id):
    try:
        funcionario = User.objects.get(pk=id)
        funcionario.is_active = False
        funcionario.save(update_fields=["is_active"])
        messages.success(request, "Funcionário excluído com sucesso.")
    except User.DoesNotExist:
        messages.error(request, "Funcionário não encontrado.")

    return redirect("funcionarios")


@login_required
def ativar_funcionario(request, id):
    try:
        funcionario = User.objects.get(pk=id)
    except User.DoesNotExist:
        messages.error(request, "Funcionario não encontrado.")
        return redirect('funcionarios_inativos')

    if funcionario.is_active == False:
        funcionario.is_active = True
        funcionario.save(update_fields=["is_active"])
        messages.success(request, "Funcionário reativado com sucesso.")

    else:
        messages.info(request, "O funcionário já está ativo.")

    return redirect('funcionarios_inativos')


@login_required
def ordenar_funcionarios_view(request, campo):
    busca = request.GET.get('busca', '')
    ativo_param = request.GET.get('ativo', 'true').lower()
    ativo = ativo_param == 'true'
    campo_ordencao = ORDER_FUNCIONARIO_LOOKUP[campo]

    funcionarios = User.objects.filter(is_active=ativo)

    if busca:
        funcionarios = funcionarios.filter(username__icontains=busca)

    funcionarios = funcionarios.order_by(campo_ordencao)

    dados = {
        'funcionarios': funcionarios,
        'ativos': ativo,
        'query': busca,
    }

    return render(request, 'funcionarios/index.html', dados)


# Login e Logout
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        verificacao_user = authenticate(
            request, username=username, password=password)

        if verificacao_user is not None:
            login(request, verificacao_user)
            return redirect('reservas:reservas')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'funcionarios/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
