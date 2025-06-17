from django import forms
from .models import Reserva


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
