from django import template

register = template.Library()


@register.filter
def cargo_nome(user, texto_fallback="Sem grupo"):

    grupo = user.groups.first()
    return grupo.name if grupo else texto_fallback
