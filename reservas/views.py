from django.shortcuts import render, redirect
from .models import Reserva
from .forms import ReservaForm


def reservas(request):
    query = request.GET.get('busca', '')

    if query:
        reservas = Reserva.objects.filter(cliente__nome__icontains=query)
    else:
        reservas = Reserva.objects.all()

    dados = {
        "reservas": reservas,
        "query": query,
    }

    return render(request, 'reservas/index.html', dados)


def cadastrar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservas')
        else:
            print(form.errors)
    else:
        form = ReservaForm()
        dados = {
            'form': form,
        }

    return render(request, 'reservas/cadastrar_reserva.html', dados)
