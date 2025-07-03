from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.calibus.forms import TravelForm
from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.calibus.models import Travel


class TravelListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Travel
    template_name = "travel/list.html"
    permission_required = "view_travel"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Travel.objects.all():
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Viajes"
        context["create_url"] = reverse_lazy("calibus:travel_create")
        context["list_url"] = reverse_lazy("calibus:travel_list")
        context["entity"] = "Viajes"
        context["parent"] = "empresa"
        context["segment"] = "viaje"
        return context


class TravelCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Travel
    form_class = TravelForm
    template_name = "travel/create.html"
    success_url = reverse_lazy("calibus:travel_list")
    permission_required = "add_travel"
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
        context["title"] = "Creación de un viaje"
        context["entity"] = "Viajes"
        context["list_url"] = self.success_url
        context["action"] = "add"
        return context


class TravelUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Travel
    form_class = TravelForm
    template_name = "travel/create.html"
    success_url = reverse_lazy("calibus:travel_list")
    permission_required = "change_travel"
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
        context["title"] = "Edición de un viaje"
        context["entity"] = "Viajes"
        context["list_url"] = self.success_url
        context["action"] = "edit"
        return context


class TravelDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Travel
    template_name = "travel/delete.html"
    success_url = reverse_lazy("calibus:travel_list")
    permission_required = "delete_travel"
    url_redirect = success_url

    @method_decorator(login_required)
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
        context["title"] = "Eliminación de un viaje"
        context["entity"] = "Viajes"
        context["list_url"] = self.success_url
        return context
