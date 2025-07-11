from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View

from core.calibus.forms import ClientForm
from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.calibus.models import Client


class ClientListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Client
    template_name = "client/list.html"
    permission_required = "view_client"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Client.objects.all():
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Clientes"
        context["create_url"] = reverse_lazy("calibus:client_create")
        context["list_url"] = reverse_lazy("calibus:client_list")
        context["entity"] = "Clientes"
        context["segment"] = "cliente"
        return context


class ClientCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "client/create.html"
    success_url = reverse_lazy("calibus:client_list")
    permission_required = "add_client"
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
        context["title"] = "Creación un Cliente"
        context["entity"] = "Clientes"
        context["list_url"] = self.success_url
        context["action"] = "add"
        return context


class ClientUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "client/create.html"
    success_url = reverse_lazy("calibus:client_list")
    permission_required = "change_client"
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
        context["title"] = "Edición un Cliente"
        context["entity"] = "Clientes"
        context["list_url"] = self.success_url
        context["action"] = "edit"
        return context


class ClientDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Client
    template_name = "client/delete.html"
    success_url = reverse_lazy("calibus:client_list")
    permission_required = "delete_client"
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
        context["title"] = "Eliminación de un Cliente"
        context["entity"] = "Clientes"
        context["list_url"] = self.success_url
        return context


class ClientAutocompleteView(View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get("term", "")
        results = []
        if term:
            clients = Client.objects.filter(names__icontains=term)[:20]
            for client in clients:
                results.append(
                    {
                        "id": client.id,
                        "text": f"{client.names} {client.surnames}".strip(),
                    }
                )
        return JsonResponse({"results": results})
