from django.contrib.auth.mixins import LoginRequiredMixin
from core.calibus.mixins import ValidatePermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse

from django.views.generic import CreateView

from core.calibus.models import Parcel
from core.calibus.forms import ParcelForm


class ParcelCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Parcel
    form_class = ParcelForm
    template_name = 'parcel/create.html'
    success_url = reverse_lazy('index')
    permission_required = 'calibus.add_parcel'
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
        context['title'] = 'Registrar Encomienda'
        context['entity'] = 'Encomiendas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
