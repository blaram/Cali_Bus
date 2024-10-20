from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.calibus.forms import RoleForm
from core.calibus.models import Role


class RoleListView(ListView):
    model = Role
    template_name = 'role/list.html'

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
                for i in Role.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Roles'
        context['create_url'] = reverse_lazy('calibus:role_create')
        context['list_url'] = reverse_lazy('calibus:role_list')
        context['entity'] = 'Roles'
        return context


class RoleCreateView(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'role/create.html'
    success_url = reverse_lazy('calibus:role_list')

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
            # data = rol = Role.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear nuevo Rol'
        context['entity'] = 'Roles'
        context['list_url'] = reverse_lazy('calibus:role_list')
        context['action'] = 'add'
        return context


class RoleUpdateView(UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'role/create.html'
    success_url = reverse_lazy('calibus:role_list')

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
        context['title'] = 'Editar Rol'
        context['entity'] = 'Roles'
        context['list_url'] = reverse_lazy('calibus:role_list')
        context['action'] = 'edit'
        return context


class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'role/delete.html'
    success_url = reverse_lazy('calibus:role_list')

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
        context['title'] = 'Eliminar Rol'
        context['entity'] = 'Roles'
        context['list_url'] = reverse_lazy('calibus:role_list')
        return context


class RoleFormView(FormView):
    form_class = RoleForm
    template_name = 'role/create.html'
    success_url = reverse_lazy('calibus:role_list')

    def form_valid(self, form):
        print(form.is_valid())
        print(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.is_valid())
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Form | Rol'
        context['entity'] = 'Roles'
        context['list_url'] = reverse_lazy('calibus:role_list')
        context['action'] = 'add'
        return context
