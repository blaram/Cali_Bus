from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy  # Add this import
from django.http import JsonResponse  # Add this import
from django.utils.decorators import method_decorator  # Add this import
from django.views.decorators.csrf import csrf_exempt  # Add this import

from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.calibus.forms import TicketForm  # Add this import, adjust the path if needed
from core.calibus.models import (
    Ticket,
    Travel,
)  # Add this import, adjust the path if needed


class TravelSaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Travel
    template_name = "ticket/travel_sale_list.html"  # Usa tu template para la venta
    permission_required = "calibus.view_travel"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                # Puedes filtrar solo viajes disponibles si lo deseas:
                for i in Travel.objects.filter(status="active"):
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Venta de Pasajes - Viajes Disponibles"
        context["list_url"] = reverse_lazy("calibus:travel_sale_list")
        context["entity"] = "Venta de Pasajes"
        context["parent"] = "empresa"
        context["segment"] = "venta_pasajes"
        return context


class TicketCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "ticket/create.html"
    success_url = reverse_lazy("index")
    permission_required = "calibus.add_ticket"
    url_redirect = success_url

    def get_initial(self):
        initial = super().get_initial()
        travel_id = self.request.GET.get("travel")
        if travel_id:
            initial["travelID"] = travel_id
        return initial

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
        travel_id = self.request.GET.get("travel")
        if travel_id:
            try:
                travel = Travel.objects.get(pk=travel_id)
                bus = travel.busID
                context["travel"] = travel
                context["bus"] = bus
                context["total_seats"] = bus.capacity
                print("DEBUG bus.capacity:", bus.capacity)  # <-- Agrega esto

            except Travel.DoesNotExist:
                context["travel"] = None
                context["bus"] = None
                context["total_seats"] = 0
        else:
            context["travel"] = None
            context["bus"] = None
            context["total_seats"] = 0
        return context
