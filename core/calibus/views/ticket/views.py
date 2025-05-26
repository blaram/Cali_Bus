from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy  # Add this import
from django.http import JsonResponse  # Add this import

from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.calibus.forms import TicketForm  # Add this import, adjust the path if needed
from core.calibus.models import Ticket  # Add this import, adjust the path if needed


class TicketCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "ticket/create.html"
    success_url = reverse_lazy("index")
    permission_required = "calibus.add_ticket"
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "add":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Registro de Pasajes"
        context["entity"] = "Pasajes"
        context["list_url"] = self.success_url
        context["action"] = "add"
        return context
