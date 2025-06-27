from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.views import View
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from collections import defaultdict
from django.template.loader import get_template
from django.conf import settings
import os
from xhtml2pdf import pisa
from datetime import date
from decimal import Decimal

from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.calibus.forms import TicketForm
from core.calibus.models import Ticket, Travel, TicketDetail, DailyCashBox, CashMovement


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
        context["parent"] = "pasajes"
        context["segment"] = "venta_pasajes"
        return context


class TicketCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "ticket/create.html"
    success_url = reverse_lazy("calibus:ticket_create")
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

                    reservation_ticket_id = body.get("reservation_ticket_id")
                    if reservation_ticket_id:
                        # Actualiza el ticket y sus detalles a vendido
                        ticket = Ticket.objects.get(id=reservation_ticket_id)
                        ticket.ticket_type = "vendido"
                        ticket.total_price = ticket_data["total_price"]
                        ticket.save()
                        data["ticket_id"] = ticket.id
                        # Actualiza los datos de los ocupantes (TicketDetail) al vender una reserva
                        for detail in details:
                            seat_number = detail["seat_number"]
                            passenger_id = detail["passengerID"]
                            # Busca el TicketDetail correspondiente a este asiento y ticket
                            ticket_detail = TicketDetail.objects.get(
                                ticketID=ticket, seat_number=seat_number
                            )
                            ticket_detail.passengerID_id = passenger_id
                            # Si tienes más campos a actualizar, agrégalos aquí
                            ticket_detail.save()
                        # Actualiza los detalles del ticket
                        if ticket.ticket_type == "vendido":
                            payment_method = body.get("payment_method")
                            if not payment_method:
                                data["error"] = (
                                    "Debe seleccionar un método de pago para la venta."
                                )
                                raise Exception(data["error"])
                            cashbox = DailyCashBox.objects.filter(
                                date=date.today(), status="open"
                            ).first()
                            if not cashbox:
                                data["error"] = (
                                    "No existe una caja diaria abierta para hoy. No se puede registrar el movimiento de caja."
                                )
                                raise Exception(data["error"])
                            description = f"Venta de pasaje a {ticket.travelID.routeID.destination} para {ticket.clientID.names} {ticket.clientID.surnames}"
                            CashMovement.objects.create(
                                cashboxID=cashbox,
                                movement_type="income",
                                amount=ticket.total_price,
                                payment_method=payment_method,
                                description=description,
                                ticket_id=ticket.id,
                            )
                            cashbox.total_income += Decimal(str(ticket.total_price))
                            cashbox.final_balance = (
                                cashbox.total_income - cashbox.total_expenses
                            )
                            cashbox.save()
                        # Si quieres, puedes actualizar los detalles aquí si es necesario
                        data["message"] = "Reserva vendida correctamente."
                    else:
                        form = TicketForm(ticket_data)
                        if form.is_valid():
                            ticket = form.save()
                            data["ticket_id"] = ticket.id
                            # Guarda los detalles del ticket
                            for detail in details:
                                TicketDetail.objects.create(
                                    ticketID=ticket,
                                    seat_number=detail["seat_number"],
                                    passengerID_id=detail["passengerID"],
                                    price=detail["price"],
                                )
                            # Solo si el ticket es vendido
                            if ticket.ticket_type == "vendido":
                                payment_method = body.get("payment_method")
                                if not payment_method:
                                    data["error"] = (
                                        "Debe seleccionar un método de pago para la venta."
                                    )
                                    raise Exception(data["error"])
                                # Obtén la caja diaria activa (abierta) del día
                                cashbox = DailyCashBox.objects.filter(
                                    date=date.today(), status="open"
                                ).first()
                                if not cashbox:
                                    data["error"] = (
                                        "No existe una caja diaria abierta para hoy. No se puede registrar el movimiento de caja."
                                    )
                                    raise Exception(data["error"])
                                description = f"Venta de pasaje a {ticket.travelID.routeID.destination} para {ticket.clientID.names} {ticket.clientID.surnames}"
                                CashMovement.objects.create(
                                    cashboxID=cashbox,
                                    movement_type="income",
                                    amount=ticket.total_price,
                                    payment_method=payment_method,
                                    description=description,
                                    ticket_id=ticket.id,
                                )
                                cashbox.total_income += ticket.total_price
                                cashbox.final_balance = (
                                    cashbox.total_income - cashbox.total_expenses
                                )
                                cashbox.save()

                            data["message"] = (
                                "Ticket y detalles guardados correctamente."
                            )
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
        context["segment"] = "venta_pasajes"
        context["parent"] = "pasajes"
        travel_id = self.request.GET.get("travel")
        if travel_id:
            try:
                travel = Travel.objects.get(pk=travel_id)
                bus = travel.busID
                context["travel"] = travel
                context["bus"] = bus
                context["total_seats"] = bus.capacity

                sold_seats = TicketDetail.objects.filter(
                    ticketID__travelID=travel, ticketID__ticket_type="vendido"
                ).values_list("seat_number", flat=True)
                reserved_seats = TicketDetail.objects.filter(
                    ticketID__travelID=travel, ticketID__ticket_type="reservado"
                ).values_list("seat_number", flat=True)
                context["sold_seats"] = list(sold_seats)
                context["reserved_seats"] = list(reserved_seats)

                # --- Agrupar reservas por cliente y ticket id ---
                reserved_details = TicketDetail.objects.filter(
                    ticketID__travelID=travel, ticketID__ticket_type="reservado"
                ).select_related("passengerID", "ticketID")
                reservations_by_client_ticket = defaultdict(list)
                client_map = {}
                ticket_map = {}
                for detail in reserved_details:
                    # Usa el cliente principal del ticket si no hay passengerID
                    client_id = (
                        detail.passengerID.id
                        if detail.passengerID
                        else detail.ticketID.clientID.id
                    )
                    client_obj = (
                        detail.passengerID
                        if detail.passengerID
                        else detail.ticketID.clientID
                    )
                    key = (client_id, detail.ticketID.id)
                    reservations_by_client_ticket[key].append(detail.seat_number)
                    client_map[client_id] = client_obj
                    ticket_map[detail.ticketID.id] = detail.ticketID
                context_list = []
                for (
                    client_id,
                    ticket_id,
                ), seats in reservations_by_client_ticket.items():
                    detail_obj = reserved_details.filter(ticketID_id=ticket_id).first()
                    context_list.append(
                        {
                            "client": client_map[client_id],
                            "seats": seats,
                            "ticket_id": ticket_id,
                            "seat_price": detail_obj.price if detail_obj else 0,
                        }
                    )
                context["reservations_by_client"] = context_list
                # Lista de pasajeros del bus (tickets vendidos para este viaje)
                passenger_details = (
                    TicketDetail.objects.filter(
                        ticketID__travelID=travel, ticketID__ticket_type="vendido"
                    )
                    .select_related("passengerID", "ticketID")
                    .order_by("seat_number")
                )

                context["bus_passenger_list"] = [
                    {
                        "seat": detail.seat_number,
                        "passenger": (
                            f"{detail.passengerID.names} {detail.passengerID.surnames}"
                            if detail.passengerID
                            else ""
                        ),
                        "nacionalidad": (
                            detail.passengerID.nationality if detail.passengerID else ""
                        ),
                        "fecha_nacimiento": (
                            detail.passengerID.date_of_birth
                            if detail.passengerID
                            else ""
                        ),
                        "documento": (
                            detail.passengerID.ci if detail.passengerID else ""
                        ),
                        "destino": (
                            detail.ticketID.travelID.routeID.destination
                            if detail.ticketID
                            and detail.ticketID.travelID
                            and detail.ticketID.travelID.routeID
                            else ""
                        ),
                        "ticket_id": detail.ticketID.id,
                        "detail_id": detail.id,
                    }
                    for detail in passenger_details
                ]
            except Travel.DoesNotExist:
                context["travel"] = None
                context["bus"] = None
                context["total_seats"] = 0
                context["sold_seats"] = []
                context["reserved_seats"] = []
                context["reservations_by_client"] = []
        else:
            context["travel"] = None
            context["bus"] = None
            context["total_seats"] = 0
            context["sold_seats"] = []
            context["reserved_seats"] = []
            context["reservations_by_client"] = []
        return context


class TicketPassengerPdfView(View):
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATICFILES_DIRS[0]
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception("El recurso %s no existe" % path)
        return path

    def get(self, request, detail_id, *args, **kwargs):
        try:
            detail = TicketDetail.objects.select_related(
                "ticketID", "ticketID__travelID", "passengerID"
            ).get(pk=detail_id)
            ticket = detail.ticketID
            travel = ticket.travelID
            context = {
                "details": [detail],  # lista de un solo detalle
                "ticket": ticket,
                "travel": travel,
                "logo": "{}{}".format(settings.STATIC_URL, "img/logo_calibus.png"),
            }
            template = get_template("ticket/ticket_list_pdf.html")
            html = template.render(context)
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = (
                f'inline; filename="boleto_{detail_id}.pdf"'
            )
            pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except Exception as e:
            return HttpResponse("Ocurrió un error al generar el PDF: %s" % str(e))


class TicketListPdfView(View):
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATICFILES_DIRS[0]
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception("El recurso %s no existe" % path)
        return path

    def get(self, request, ticket_id, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
            details = TicketDetail.objects.filter(ticketID=ticket).select_related(
                "passengerID"
            )
            context = {
                "ticket": ticket,
                "client": ticket.clientID,
                "travel": ticket.travelID,
                "details": details,
                "logo": "{}{}".format(settings.STATIC_URL, "img/logo_calibus.png"),
            }
            template = get_template(
                "ticket/ticket_list_pdf.html"
            )  # Debes crear este template
            html = template.render(context)
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = (
                f'inline; filename="ticket_{ticket_id}.pdf"'
            )
            pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except Exception as e:
            return HttpResponse("Ocurrió un error al generar el PDF: %s" % str(e))


class PassengerListPdfView(View):
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATICFILES_DIRS[0]
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception("El recurso %s no existe" % path)
        return path

    def get(self, request, *args, **kwargs):
        try:
            # travel_id = kwargs.get("travel_id")
            travel = Travel.objects.get(pk=self.kwargs["travel_id"])
            bus = travel.busID
            passenger_details = (
                TicketDetail.objects.filter(
                    ticketID__travelID=travel, ticketID__ticket_type="vendido"
                )
                .select_related("passengerID", "ticketID")
                .order_by("seat_number")
            )
            context = {
                "travel": travel,
                "bus": bus,
                "logo": "{}{}".format(settings.STATIC_URL, "img/logo_calibus.png"),
                "bus_passenger_list": [
                    {
                        "seat": detail.seat_number,
                        "passenger": (
                            f"{detail.passengerID.names} {detail.passengerID.surnames}"
                            if detail.passengerID
                            else ""
                        ),
                        "nacionalidad": (
                            detail.passengerID.nationality if detail.passengerID else ""
                        ),
                        "fecha_nacimiento": (
                            detail.passengerID.date_of_birth
                            if detail.passengerID
                            else ""
                        ),
                        "documento": (
                            detail.passengerID.ci if detail.passengerID else ""
                        ),
                        "destino": (
                            detail.ticketID.travelID.routeID.destination
                            if detail.ticketID
                            and detail.ticketID.travelID
                            and detail.ticketID.travelID.routeID
                            else ""
                        ),
                        "detail_id": detail.id,
                    }
                    for detail in passenger_details
                ],
            }
            template = get_template("ticket/passenger_list_pdf.html")
            html = template.render(context)
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'inline; filename="lista_pasajeros.pdf"'
            pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except Exception as e:
            return HttpResponse("Ocurrió un error al generar el PDF: %s" % str(e))
