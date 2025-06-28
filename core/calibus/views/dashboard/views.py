from django.views.generic import TemplateView
from datetime import datetime
from core.calibus.models import Ticket  # Import the Ticket model
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce


class DashboardView(TemplateView):
    template_name = "dashboard.html"

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["panel"] = "Panel de administrador"
        print(self.get_graph_sales_year_month())
        context["graph_sales_year_month"] = self.get_graph_sales_year_month()
        return context
