from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarifa
from .forms import TarifaForm
from django.contrib.auth.decorators import user_passes_test, login_required


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def lista_tarifas(request):
    tarifas = Tarifa.objects.select_related(
        'tipo_quarto').order_by('-data_inicio')
    return render(request, 'tarifas/lista.html', {'tarifas': tarifas})


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
