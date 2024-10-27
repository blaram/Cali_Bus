from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse

from core.calibus.models import Bus
from core.calibus.forms import BusForm


class BusListView(ListView):
    model = Bus
    template_name = 'bus/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Bus.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Buses'
        context['create_url'] = reverse_lazy('calibus:bus_create')
        context['list_url'] = reverse_lazy('calibus:bus_list')
        context['entity'] = 'Buses'
        return context


class BusCreateView(CreateView):
    model = Bus
    form_class = BusForm
    template_name = 'bus/create.html'
    success_url = reverse_lazy('calibus:bus_list')

    @method_decorator(login_required)
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
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Insertar nuevo Bus'
        context['entity'] = 'Buses'
        context['list_url'] = reverse_lazy('calibus:bus_list')
        context['action'] = 'add'
        return context


class BusUpdateView(UpdateView):
    model = Bus
    form_class = BusForm
    template_name = 'bus/create.html'
    success_url = reverse_lazy('calibus:bus_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                # rol = self.get_object()
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Bus'
        context['entity'] = 'Buses'
        context['list_url'] = reverse_lazy('calibus:bus_list')
        context['action'] = 'edit'
        return context


class BusDeleteView(DeleteView):
    model = Bus
    template_name = 'bus/delete.html'
    success_url = reverse_lazy('calibus:bus_list')

    @method_decorator(login_required)
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
        context['title'] = 'Eliminar Bus'
        context['entity'] = 'Buses'
        context['list_url'] = reverse_lazy('calibus:bus_list')
        return context
