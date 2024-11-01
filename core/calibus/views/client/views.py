from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.calibus.models import Client
from core.calibus.forms import ClientForm


class ClientView(TemplateView):
    template_name = 'client/list.html'

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
                for i in Client.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                cli = Client()
                cli.names = request.POST['names']
                cli.surnames = request.POST['surnames']
                cli.ci = request.POST['ci']
                cli.phone = request.POST['phone']
                cli.email = request.POST['email']
                cli.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('calibus:client')
        context['entity'] = 'Clientes'
        context['form'] = ClientForm()
        return context
