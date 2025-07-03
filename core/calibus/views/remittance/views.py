from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.calibus.models import Remittance
from core.calibus.forms import RemittanceForm


class RemittanceListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Remittance
    template_name = "remittance/list.html"
    permission_required = "view_remittance"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Remittance.objects.all():
                    data.append(i.toJSON())
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Giros"
        context["create_url"] = reverse_lazy("calibus:remittance_create")
        context["list_url"] = reverse_lazy("calibus:remittance_list")
        context["entity"] = "Giros"
        context["parent"] = "envios"
        context["segment"] = "giro"
        return context


class RemittanceCreateView(
    LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView
):
    model = Remittance
    form_class = RemittanceForm
    template_name = "remittance/create.html"
    success_url = reverse_lazy("index")
    permission_required = "add_remittance"
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "add":
                form = self.get_form()
                if form.is_valid():
                    instance = form.save()
                    data["success"] = "Remesa guardada correctamente"
                    data["id"] = (
                        instance.id
                    )  # puedes devolver el id u otros datos si quieres
                else:
                    data["error"] = form.errors.as_json()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Envío de Giros"
        context["entity"] = "Giros"
        context["list_url"] = self.success_url
        context["action"] = "add"
        return context
