from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.calibus.forms import TicketForm
from core.calibus.models import Ticket, Travel, TicketDetail


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
    success_url = reverse_lazy("calibus:travel_sale_list")
    permission_required = "calibus.add_ticket"
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get("action", None)
            if action == "add":
                with transaction.atomic():
                    ticket_data = body.get("ticket", {})
                    details = body.get("details", [])
                    ticket_data["total_price"] = sum(
                        float(detail["price"]) for detail in details
                    )
                    print("DEBUG ticket_data:", ticket_data)
                    print("DEBUG detalles:", details)
                    print("DEBUG total calculado:", ticket_data["total_price"])
                    form = TicketForm(ticket_data)
                    if form.is_valid():
                        ticket = form.save()
                        for detail in details:
                            TicketDetail.objects.create(
                                ticketID=ticket,
                                seat_number=detail["seat_number"],
                                passengerID_id=detail["passengerID"],
                                price=detail["price"],
                            )
                        data["message"] = "Ticket y detalles guardados correctamente."
                    else:
                        data["error"] = form.errors
            else:
                data["error"] = "No ha ingresado a ninguna opción válida."
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
