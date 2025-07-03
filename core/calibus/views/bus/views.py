from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.calibus.forms import BusForm
from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.calibus.models import Bus


class BusListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Bus
    template_name = "bus/list.html"
    permission_required = "view_bus"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Bus.objects.all():
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Buses"
        context["create_url"] = reverse_lazy("calibus:bus_create")
        context["list_url"] = reverse_lazy("calibus:bus_list")
        context["entity"] = "Buses"
        context["parent"] = "empresa"
        context["segment"] = "bus"
        return context


class BusCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Bus
    form_class = BusForm
    template_name = "bus/create.html"
    success_url = reverse_lazy("calibus:bus_list")
    permission_required = "add_bus"
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
        context["title"] = "Creación de un Bus"
        context["entity"] = "Buses"
        context["list_url"] = self.success_url
        context["action"] = "add"
        return context


class BusUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Bus
    form_class = BusForm
    template_name = "bus/create.html"
    success_url = reverse_lazy("calibus:bus_list")
    permission_required = "change_bus"
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "edit":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edición de un Bus"
        context["entity"] = "Buses"
        context["list_url"] = self.success_url
        context["action"] = "edit"
        return context


class BusDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Bus
    template_name = "bus/delete.html"
    success_url = reverse_lazy("calibus:bus_list")
    permission_required = "delete_bus"
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminación de un Bus"
        context["entity"] = "Buses"
        context["list_url"] = self.success_url
        return context
