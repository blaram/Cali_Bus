from django.contrib.auth.mixins import LoginRequiredMixin
from core.calibus.mixins import ValidatePermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction

from django.views.generic import CreateView, ListView

from core.calibus.models import Parcel, ParcelItem
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
            # Procesar datos JSON desde el cuerpo de la solicitud
            body = json.loads(request.body)
            print("Datos recibidos en JSON:", body)  # Depuración

            action = body.get('action', None)
            print("Acción recibida:", action)  # Depuración
            if action == 'add':
                with transaction.atomic():
                    # Recalcular el total en el backend
                    items = body.get('items', [])
                    total_calculated = sum(
                        float(item['shipping_cost']) for item in items
                    )

                    # Comparar con el total enviado desde el frontend
                    total_sent =float(body.get('total', 0.00))
                    if total_calculated != total_sent:
                        data['error'] = 'El total enviado no coincide con el total calculado.'
                        return JsonResponse(data)

                    # Procesar el formulario de Parcel
                    parcel_form = ParcelForm(body)
                    if parcel_form.is_valid():
                        parcel = parcel_form.save(commit=False)  # No guardar aún
                        parcel.total = total_calculated
                        parcel.save()

                        # Procesar los datos de ParcelItem enviados como JSON
                        for item_data in items:
                            ParcelItem.objects.create(
                                parcelID=parcel,
                                description=item_data['description'],
                                quantity=item_data['quantity'],
                                weight=item_data['weight'],
                                declared_value=item_data['declared_value'],
                                shipping_cost=item_data['shipping_cost'],
                            )
                        data['message'] = 'Encomienda y artículos guardados correctamente.'
                    else:
                        data['error'] = parcel_form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción válida.'
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
