from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.calibus.forms import RouteForm
from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.calibus.models import Route


class RouteListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Route
    template_name = 'route/list.html'
    permission_required = 'calibus.view_route'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Route.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de rutas'
        context['create_url'] = reverse_lazy('calibus:route_create')
        context['list_url'] = reverse_lazy('calibus:route_list')
        context['entity'] = 'Rutas'
        context['parent'] = 'empresa'
        context['segment'] = 'ruta'
        return context


class RouteCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Route
    form_class = RouteForm
    template_name = 'route/create.html'
    success_url = reverse_lazy('calibus:route_list')
    permission_required = 'calibus.add_route'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una ruta'
        context['entity'] = 'Rutas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['parent'] = 'empresa'
        context['segment'] = 'ruta'
        return context


class RouteUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Route
    form_class = RouteForm
    template_name = 'route/create.html'
    success_url = reverse_lazy('calibus:route_list')
    permission_required = 'calibus.change_route'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una ruta'
        context['entity'] = 'Rutas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['parent'] = 'empresa'
        context['segment'] = 'ruta'
        return context


class RouteDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Route
    template_name = 'route/delete.html'
    success_url = reverse_lazy('calibus:route_list')
    permission_required = 'calibus.delete_route'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una ruta'
        context['entity'] = 'Rutas'
        context['list_url'] = self.success_url
        context['parent'] = 'empresa'
        context['segment'] = 'ruta'
        return context
