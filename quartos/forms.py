# forms.py
from django import forms
from .models import TipoQuarto, Quarto


class TipoQuartoForm(forms.ModelForm):
    class Meta:
        model = TipoQuarto
        fields = ['nome', 'descricao', 'capacidade']


class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero', 'andar', 'descricao', 'status', 'tipo']
