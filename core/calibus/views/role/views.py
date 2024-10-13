from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from core.calibus.forms import RoleForm
from core.calibus.models import Role


def role_list(request):
    data = {
        'title': 'Listado de Roles',
        'roles': Role.objects.all()
    }
    return render(request, 'role/list.html', data)


class RoleListView(ListView):
    model = Role
    template_name = 'role/list.html'

    # def get_queryset(self):
    #     return Role.objects.all()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # if request.method == 'GET':
        #     return redirect('calibus:role_list2')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = rol = Role.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

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

    #     print(request.POST)
    #     form = RoleForm(request.POST)
    #     if form.is_valid():
    #         # form.save()
    #         return HttpResponseRedirect(self.success_url)
    #     # else:
    #     #     return render(request, self.template_name, {'form': form})
    #     print(form.errors)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Rol'
        context['entity'] = 'Roles'
        context['list_url'] = reverse_lazy('calibus:role_list')
        return context
