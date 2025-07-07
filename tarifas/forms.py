from django import forms
from .models import Tarifa


class TarifaForm(forms.ModelForm):
    data_inicio = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    data_fim = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Tarifa
        fields = ['tipo_quarto', 'valor', 'temporada',
                  'data_inicio', 'data_fim', 'ativa']
