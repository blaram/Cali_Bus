from django.shortcuts import render
from django.views.generic import ListView

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

    def get_queryset(self):
        return Role.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Roles'
        return context
