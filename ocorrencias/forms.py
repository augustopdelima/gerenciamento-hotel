from django import forms
from .models import Ocorrencia


class OcorrenciaForm(forms.ModelForm):
    data_resolvido = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Ocorrencia
        fields = ['quarto', 'descricao', 'resolvido', 'data_resolvido']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
