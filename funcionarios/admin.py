from django.contrib import admin

from funcionarios.models import Cargo, Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ["nome", "ativo", "email", "cargo__nome_funcao"]
    list_filter = ["ativo", "cargo__nome_funcao"]
    search_fields = ["nome", "ativo", "email", "cargo__nome_funcao"]


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ["nome_funcao"]
    list_filter = ["nome_funcao"]
    search_fields = ["nome_funcao"]
