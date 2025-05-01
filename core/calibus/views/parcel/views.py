from django.contrib.auth.mixins import LoginRequiredMixin
from core.calibus.mixins import ValidatePermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.views.generic import CreateView, ListView

from core.calibus.models import Parcel
from core.calibus.forms import ParcelForm


class ParcelListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Parcel
    template_name = 'parcel/list.html'
    permission_required = 'calibus.view_parcel'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Parcel.objects.all():
                    data.append(i.toJSON())  # Asegúrate de que el modelo Parcel tenga un método `toJSON`
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Encomiendas'
        context['create_url'] = reverse_lazy('calibus:parcel_create')
        context['list_url'] = reverse_lazy('calibus:parcel_list')
        context['entity'] = 'Encomiendas'
        context['parent'] = 'envios'
        context['segment'] = 'encomienda'
        return context


class ParcelCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Parcel
    form_class = ParcelForm
    template_name = 'parcel/create.html'
    success_url = reverse_lazy('index')
    permission_required = 'calibus.add_parcel'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                parcels = json.loads(request.POST.get('parcels', '[]'))
                for parcel_data in parcels:
                    parcel = Parcel()
                    parcel.senderID_id = parcel_data['senderID']
                    parcel.receiverID_id = parcel_data['receiverID']
                    parcel.travelID_id = parcel_data['travelID']
                    parcel.date_joined = parcel_data['date_joined']
                    parcel.description = parcel_data['description']
                    parcel.weight = parcel_data['weight']
                    parcel.declared_value = parcel_data['declared_value']
                    parcel.shipping_cost = parcel_data['shipping_cost']
                    parcel.status = True
                    parcel.save()
                data['message'] = 'Encomiendas guardadas correctamente.'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Encomienda'
        context['entity'] = 'Encomiendas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
