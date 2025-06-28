from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from core.reports.forms import ReportForm
from core.calibus.models import Ticket  # Import the Ticket model
from core.calibus.models import CashMovement  # Import the CashMovement model

from datetime import datetime
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce


# Create your views here.
class ReportSaleView(TemplateView):
    template_name = "sale/report.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "search_report":
                data = []
                start_date = request.POST.get("start_date", "")
                end_date = request.POST.get("end_date", "")
                search = Ticket.objects.filter(ticket_type="vendido")
                if len(start_date) and len(end_date):
                    start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
                    end_date = datetime.strptime(end_date, "%d-%m-%Y").date()
                    search = search.filter(purchase_date__range=[start_date, end_date])
                for idx, t in enumerate(search, start=1):
                    cash_movement = (
                        CashMovement.objects.filter(ticket_id=t.id)
                        .order_by("-id")
                        .first()
                    )
                    payment_method = (
                        cash_movement.get_payment_method_display()
                        if cash_movement
                        else "N/A"
                    )
                    data.append(
                        [
                            idx,
                            f"{t.clientID.names} {t.clientID.surnames}",
                            t.purchase_date.strftime("%d-%m-%Y"),
                            payment_method,
                            t.ticketdetail_set.count(),
                            format(t.total_price, ".2f"),
                        ]
                    )
                total = search.aggregate(
                    r=Coalesce(Sum("total_price"), 0, output_field=DecimalField())
                ).get("r")

                data.append(
                    [
                        "",
                        "",
                        "",
                        "",
                        "Total",
                        format(total, ".2f"),
                    ]
                )

            else:
                data["error"] = "Ha ocurrido un error."
        except Exception as e:
            return JsonResponse({"error": str(e)}, safe=False)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reporte de Ventas"
        context["entity"] = "Reportes"
        context["list_url"] = reverse_lazy("sale_report")
        context["form"] = ReportForm()
        # context["subtitle"] = "Reporte de Ventas de Pasajes"
        # context["description"] = "Genera un reporte detallado de las ventas de pasajes."
        return context
        return context
