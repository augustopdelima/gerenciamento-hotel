from django.shortcuts import redirect

class AtendenteAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name="Atendente").exists():
                allowed_apps = ["ocorrencias", "reservas", "clientes"]
                app_name = view_func.__module__.split('.')[0]

                logout_views = [
                    "funcionarios.views.logout_view",
                ]
                view_path = f"{view_func.__module__}.{view_func.__name__}"
                if (
                    app_name not in allowed_apps
                    and view_path not in logout_views
                ):
                    return redirect("reservas:reservas")
        return None