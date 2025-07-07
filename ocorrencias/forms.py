from django import forms
from .models import Ocorrencia
from quartos.models import Quarto


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


class RelatorioOcorrencias(forms.Form):
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

    quarto = forms.ModelChoiceField(
        required=False,
        label="Quarto",
        queryset=Quarto.objects.order_by('numero'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    resolvido = forms.ChoiceField(
        required=False,
        label="Resolvido",
        choices=[
            ('', 'Todos'),
            ('sim', 'Resolvidos'),
            ('nao', 'Pendentes'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    criado_por = forms.CharField(
        required=False,
        label="Criado por (usuário)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username'
        })
    )
