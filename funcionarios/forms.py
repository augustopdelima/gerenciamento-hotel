from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

MINUSCULAS = {'da', 'de', 'do', 'das', 'dos', 'e'}


def formatar_nome(nome: str) -> str:
    return ' '.join(
        p if p in MINUSCULAS else p.capitalize()
        for p in nome.lower().split()
    )


class FuncionarioForm(UserCreationForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(), label="Cargo (Grupo)")
    is_active = forms.BooleanField(
        label="Usuário ativo", required=False, initial=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email',
                  'is_active', 'password1', 'password2', 'grupo']
        labels = {
            'username': 'Usuário',
            'first_name': 'Nome',
            'email': 'E-mail',
            'password1': 'Senha',
            'password2': 'Confirmação de Senha',
            'grupo': 'Cargo (Grupo)',
            'is_active': 'Usuário ativo',
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        if user.first_name:
            user.first_name = formatar_nome(user.first_name)

        user.is_active = self.cleaned_data['is_active']

        if commit:
            user.save()
            grupo = self.cleaned_data['grupo']
            user.groups.add(grupo)

            # Libera acesso ao admin se for do grupo "Administrador"
            if grupo.name == "Administrador":
                user.is_staff = True
                user.save(update_fields=["is_staff"])

        return user
