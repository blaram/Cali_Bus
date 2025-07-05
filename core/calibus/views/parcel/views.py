from django.contrib.auth.mixins import LoginRequiredMixin
from core.calibus.mixins import ValidatePermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from datetime import date
from django.views.generic import CreateView, ListView, View

from core.calibus.models import Parcel, ParcelItem, CashMovement, DailyCashBox
from core.calibus.forms import ParcelForm
from core.calibus.choices import parcel_choices, payment_method_choices

import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa


class ParcelListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Parcel
    template_name = "parcel/list.html"
    permission_required = "view_parcel"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Parcel.objects.all():
                    data.append(
                        i.toJSON()
                    )  # Asegúrate de que el modelo Parcel tenga un método `toJSON`
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Encomiendas"
        context["create_url"] = reverse_lazy("calibus:parcel_create")
        context["list_url"] = reverse_lazy("calibus:parcel_list")
        context["entity"] = "Encomiendas"
        context["parent"] = "envios"
        context["segment"] = "encomienda"
        context["parcel_choices"] = json.dumps(dict(parcel_choices))
        return context


class ParcelCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Parcel
    form_class = ParcelForm
    template_name = "parcel/create.html"
    success_url = reverse_lazy("index")
    permission_required = "add_parcel"
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Procesar datos JSON desde el cuerpo de la solicitud
            body = json.loads(request.body)
            print("Datos recibidos en JSON:", body)  # Depuración

            action = body.get("action", None)
            print("Acción recibida:", action)  # Depuración
            if action == "add":
                with transaction.atomic():
                    # Recalcular el total en el backend
                    items = body.get("items", [])
                    total_calculated = sum(
                        float(item["shipping_cost"]) for item in items
                    )

                    # Comparar con el total enviado desde el frontend
                    total_sent = float(body.get("total", 0.00))
                    if total_calculated != total_sent:
                        data["error"] = (
                            "El total enviado no coincide con el total calculado."
                        )
                        return JsonResponse(data)

                    # Procesar el formulario de Parcel
                    parcel_form = ParcelForm(body)

                    # Obtén el método de pago del body
                    payment_method = body.get("payment_method")

                    # Obtén la caja diaria activa
                    cashbox = DailyCashBox.objects.filter(
                        status="open", date=date.today()
                    ).first()
                    print(
                        "Todas las cajas abiertas:",
                        list(DailyCashBox.objects.filter(status="open")),
                    )
                    if not cashbox:
                        data["error"] = (
                            "No hay una caja diaria abierta para registrar el movimiento de caja."
                        )
                        return JsonResponse(data)

                    if parcel_form.is_valid():
                        parcel = parcel_form.save(commit=False)  # No guardar aún
                        parcel.total = total_calculated
                        parcel.save()

                        # Obtén el método de pago del body (ajusta el nombre si es diferente)
                        # payment_method = body.get("payment_method")

                        # Obtén la caja diaria activa (ajusta el filtro según tu lógica de caja abierta)
                        # cashbox = DailyCashBox.objects.filter(status="open").last()
                        # if not cashbox:
                        #     data["error"] = (
                        #         "No hay una caja diaria abierta para registrar el movimiento de caja."
                        #     )
                        #     return JsonResponse(data)

                        print("Método de pago recibido:", payment_method)

                        # Crea el movimiento de caja
                        CashMovement.objects.create(
                            cashboxID=cashbox,
                            movement_type="ingreso",  # o el valor correspondiente de tus choices
                            amount=total_calculated,
                            payment_method=payment_method,
                            description=f"Encomienda #{parcel.id}",
                            parcel_id=parcel.id,
                        )

                        # Procesar los datos de ParcelItem enviados como JSON
                        for item_data in items:
                            ParcelItem.objects.create(
                                parcelID=parcel,
                                description=item_data["description"],
                                quantity=item_data["quantity"],
                                weight=item_data["weight"],
                                declared_value=item_data["declared_value"],
                                shipping_cost=item_data["shipping_cost"],
                            )
                        data["message"] = (
                            "Encomienda y artículos guardados correctamente."
                        )
                        data["parcel_id"] = (
                            parcel.id
                        )  # Agregar el ID de la encomienda al JSON de respuesta
                    else:
                        data["error"] = parcel_form.errors
            else:
                data["error"] = "No ha ingresado a ninguna opción válida."
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment_method_choices"] = payment_method_choices
        context["title"] = "Registrar Encomienda"
        context["entity"] = "Encomiendas"
        context["list_url"] = self.success_url
        context["action"] = "add"
        return context


@csrf_exempt
def change_status(request):
    data = {}
    try:
        if request.method == "POST" and request.POST.get("action") == "change_status":
            parcel_id = request.POST.get("id")
            current_status = request.POST.get("status")

            # Get the package by id
            parcel = Parcel.objects.get(pk=parcel_id)

            # Change the state according to the current status
            if current_status == "pending":
                parcel.status = "in_transit"
            elif current_status == "in_transit":
                parcel.status = "ready_for_pickup"
            elif current_status == "ready_for_pickup":
                parcel.status = "delivered"
            elif current_status == "delivered":
                parcel.status = "cancelled"
            elif current_status == "cancelled":
                parcel.status = "pending"

            # Save the change to the database
            parcel.save()

            data["message"] = "Estado cambiado correctamente."
        else:
            data["error"] = "Solicitud no válida."
    except Exception as e:
        data["error"] = str(e)
    return JsonResponse(data)


class ParcelReceiptPdfView(View):
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

    def get(self, request, pk, *args, **kwargs):
        try:
            template = get_template("parcel/parcel_receipt_pdf.html")
            parcel = Parcel.objects.get(pk=pk)
            items = ParcelItem.objects.filter(parcelID=parcel)
            context = {
                "parcel": parcel,
                "items": items,
                "logo": f"{settings.STATIC_URL}img/logo_calibus.png",
            }
            html = template.render(context)
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'inline; filename="parcel_receipt.pdf"'
            pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except Exception as e:
            print("Error al generar PDF:", e)
            return HttpResponse("Ocurrió un error al generar el PDF: %s" % str(e))
