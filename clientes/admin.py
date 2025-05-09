from django.contrib import admin

from clientes.models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nome", "email", "telefone"]
    list_filter = ["nome"]
    search_fields = ["nome", "telfone", "email"]
