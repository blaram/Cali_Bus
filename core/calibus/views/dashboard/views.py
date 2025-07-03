from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from core.calibus.models import Ticket, Bus
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "get_graph_sales_year_month":
                data = {
                    "name": "Porcentaje de venta",
                    "showInLegend": False,
                    "colorByPoint": True,
                    "data": self.get_graph_sales_year_month(),
                }
            elif action == "get_graph_sales_tickets_year_month":
                data = {
                    "name": "Boletos vendidos",
                    "colorByPoint": True,
                    "data": self.get_graph_sales_tickets_year_month(),
                }
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            print("AÑO USADO:", year)
            for m in range(1, 13):
                queryset = Ticket.objects.filter(
                    ticket_type="vendido",
                    purchase_date__year=year,
                    purchase_date__month=m,
                )
                print(f"Mes {m}, queryset count: {queryset.count()}")
                total = queryset.aggregate(
                    r=Coalesce(Sum("total_price"), 0, output_field=DecimalField())
                ).get("r")
                print(f"Mes {m}: {total}")
                data.append(float(total))
        except Exception as e:
            print("ERROR:", e)
            data = [0] * 12
        return data

    def get_graph_sales_tickets_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            buses = Bus.objects.all()
            total_tickets = Ticket.objects.filter(
                ticket_type="vendido",
                purchase_date__year=year,
                purchase_date__month=month,
            ).count()
            for bus in buses:
                count = Ticket.objects.filter(
                    ticket_type="vendido",
                    purchase_date__year=year,
                    purchase_date__month=month,
                    travelID__busID=bus,
                ).count()
                if count > 0 and total_tickets > 0:
                    porcentaje = (count / total_tickets) * 100
                    data.append(
                        {
                            "name": bus.license_plate,
                            "y": porcentaje,
                        }
                    )
        except Exception as e:
            print("ERROR:", e)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["panel"] = "Panel de administrador"
        print(self.get_graph_sales_year_month())
        context["graph_sales_year_month"] = self.get_graph_sales_year_month()
        return context
