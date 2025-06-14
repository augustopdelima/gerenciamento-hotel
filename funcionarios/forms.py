from django import forms
from .models import Funcionario, Cargo


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'cargo']


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nome_funcao']
