from django import forms
from .models import Reserva, STATUS_RESERVA_CHOICES
from quartos.models import TipoQuarto


class ReservaForm(forms.ModelForm):
    data_entrada = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    data_saida = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Reserva
        fields = ['data_entrada', 'data_saida', 'cliente',
                  'funcionario', 'quarto', 'status']


class RelatorioReservas(forms.Form):
    data_inicio = forms.DateField(
        required=False,
        label="Data de Início",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%d']
    )

    data_fim = forms.DateField(
        required=False,
        label="Data de Fim",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%d']
    )

    cliente = forms.CharField(
        required=False,
        label="Cliente",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome do cliente'
        })
    )

    status = forms.ChoiceField(
        required=False,
        label="Status",
        choices=[('', 'Todos')] + STATUS_RESERVA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    ativo = forms.ChoiceField(
        required=False,
        label="Ativo",
        choices=[('', 'Todos'), ('ativa', 'Ativo'), ('inativa', 'Inativo')],
        widget=forms.Select(attrs={'class': 'form-select'})

    )

    quarto = forms.ModelChoiceField(
        required=False,
        label="Tipo de Quarto",
        queryset=TipoQuarto.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
