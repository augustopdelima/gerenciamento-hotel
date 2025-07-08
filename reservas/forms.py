from django import forms
from .models import Reserva, STATUS_RESERVA_CHOICES, CheckInCheckOut
from quartos.models import TipoQuarto, Quarto
from clientes.models import Cliente
from django.contrib.auth.models import User


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
        fields = ['data_entrada', 'data_saida', 'cliente', 'quarto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # mostra apenas os quartos disponíveis
        qs = Quarto.objects.filter(
            status__in=["disponivel", "reservado", "ocupado"])

        cs = Cliente.objects.filter(ativo=True)

        # se estiver editando, garante que o quarto já associado apareça
        if self.instance.pk and self.instance.quarto:
            qs = qs | Quarto.objects.filter(pk=self.instance.quarto.pk)

        if self.instance.pk and self.instance.cliente:
            cs = cs | Cliente.objects.filter(pk=self.instance.cliente.pk)

        self.fields["quarto"].queryset = qs

        self.fields["cliente"].queryset = cs

        if self.instance.pk:
            # Adiciona o campo status dinamicamente
            self.fields['status'] = forms.ChoiceField(
                choices=Reserva._meta.get_field('status').choices,
                initial=self.instance.status,
                label="Status",
                widget=forms.Select(attrs={'class': 'form-select'})
            )

            funcionarios_qs = User.objects.filter(is_active=True)

            if self.instance.funcionario:
                funcionarios_qs = funcionarios_qs | User.objects.filter(
                    pk=self.instance.funcionario.pk)

            self.fields['funcionario'] = forms.ModelChoiceField(
                queryset=funcionarios_qs.distinct(),
                label="Funcionário",
                widget=forms.Select(attrs={'class': 'form-select'}),
                initial=self.instance.funcionario.pk if self.instance.funcionario else None,
            )


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

    quarto = forms.ModelChoiceField(
        required=False,
        label="Tipo de Quarto",
        queryset=TipoQuarto.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


class CheckInOutForm(forms.ModelForm):
    data_checkin = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        required=True
    )
    data_checkout = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        required=False
    )

    class Meta:
        model = CheckInCheckOut
        fields = ['funcionario_checkin', 'data_checkin',
                  'funcionario_checkout', 'data_checkout']


CheckInOutFormSet = forms.inlineformset_factory(
    parent_model=Reserva,
    model=CheckInCheckOut,
    form=CheckInOutForm,
    extra=0,       # 0 = só mostra se já existir; mude para 1 se quiser criar
    max_num=1,
    can_delete=False,
)
