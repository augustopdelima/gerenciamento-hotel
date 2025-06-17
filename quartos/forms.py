# forms.py
from django import forms
from .models import TipoQuarto, StatusQuarto, Quarto


class TipoQuartoForm(forms.ModelForm):
    class Meta:
        model = TipoQuarto
        fields = ['nome', 'descricao', 'capacidade',
                  'possui_varanda', 'banheiras']


class StatusQuartoForm(forms.ModelForm):
    class Meta:
        model = StatusQuarto
        fields = ['tag', 'descricao']


class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero', 'andar', 'descricao', 'status', 'tipo']
