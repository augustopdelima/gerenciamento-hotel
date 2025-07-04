from django import forms
from .models import Ocorrencia

class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ['quarto', 'descricao', 'resolvido', 'data_resolvido']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'data_resolvido': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
