from django import forms
from .models import Tarifa, TEMPORADA_CHOICES
from quartos.models import TipoQuarto


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


class RelatorioTarifas(forms.Form):
    data_inicio = forms.DateTimeField(
        required=False,
        label="Data de Início",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    data_fim = forms.DateTimeField(
        required=False,
        label="Data de Fim",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    tipo_quarto = forms.ModelChoiceField(
        required=False,
        label="Tipo de Quarto",
        queryset=TipoQuarto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    valor_minimo = forms.DecimalField(
        required=False,
        label="Valor Mínimo",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Ex: 100.00'})
    )

    valor_maximo = forms.DecimalField(
        required=False,
        label="Valor Máximo",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Ex: 500.00'})
    )

    temporada = forms.ChoiceField(
        required=False,
        label="Temporada",
        choices=[('', 'Todas')] + TEMPORADA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    ativa = forms.ChoiceField(
        required=False,
        label="Ativa",
        choices=[
            ('', 'Todas'),
            ('sim', 'Ativas'),
            ('nao', 'Inativas'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
