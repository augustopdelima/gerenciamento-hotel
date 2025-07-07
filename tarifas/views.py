from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarifa
from .forms import TarifaForm, RelatorioTarifas
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def lista_tarifas(request):
    form = RelatorioTarifas(request.GET or None)
    tarifas = Tarifa.objects.all().order_by('-data_inicio')

    if form.is_valid():
        cd = form.cleaned_data

        if cd.get("data_inicio"):
            tarifas = tarifas.filter(data_inicio__gte=cd["data_inicio"])
        if cd.get("data_fim"):
            tarifas = tarifas.filter(data_fim__lte=cd["data_fim"])
        if cd.get("tipo_quarto"):
            tarifas = tarifas.filter(tipo_quarto=cd["tipo_quarto"])
        if cd.get("valor_minimo"):
            tarifas = tarifas.filter(valor__gte=cd["valor_minimo"])
        if cd.get("valor_maximo"):
            tarifas = tarifas.filter(valor__lte=cd["valor_maximo"])
        if cd.get("temporada"):
            tarifas = tarifas.filter(temporada=cd["temporada"])
        if cd.get("ativa") == "sim":
            tarifas = tarifas.filter(ativa=True)
        elif cd.get("ativa") == "nao":
            tarifas = tarifas.filter(ativa=False)

    return render(request, "tarifas/lista.html", {
        "form": form,
        "tarifas": tarifas
    })


@login_required
@user_passes_test(is_admin)
def desativar_tarifa(request, tarifa_id):
    tarifa = get_object_or_404(Tarifa, id=tarifa_id)

    if not tarifa.ativa:
        messages.warning(request, "A tarifa já está desativada.")
    else:
        tarifa.ativa = False
        tarifa.save(update_fields=['ativa'])
        messages.success(request, "Tarifa desativada com sucesso.")

    return redirect('lista_tarifas')


@login_required
@user_passes_test(is_admin)
def ativar_tarifa(request, tarifa_id):
    tarifa = get_object_or_404(Tarifa, id=tarifa_id)

    if tarifa.ativa:
        messages.warning(request, "A tarifa já está ativa.")
    else:
        tarifa.ativa = True
        tarifa.save(update_fields=['ativa'])
        messages.success(request, "Tarifa ativada com sucesso.")

    return redirect('lista_tarifas')


@login_required
@user_passes_test(is_admin)
def nova_tarifa(request):
    if request.method == 'POST':
        form = TarifaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tarifas')
    else:
        form = TarifaForm()
    return render(request, 'tarifas/form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def editar_tarifa(request, tarifa_id):
    tarifa = get_object_or_404(Tarifa, id=tarifa_id)
    if request.method == 'POST':
        form = TarifaForm(request.POST, instance=tarifa)
        if form.is_valid():
            form.save()
            return redirect('lista_tarifas')
    else:
        form = TarifaForm(instance=tarifa)
    return render(request, 'tarifas/form.html', {'form': form})
