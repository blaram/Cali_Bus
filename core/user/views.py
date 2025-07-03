from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

from core.calibus.forms import RouteForm
from core.calibus.mixins import ValidatePermissionRequiredMixin
from core.user.models import User
from core.user.forms import UserForm, UserProfileForm
from django.contrib.auth.models import Group


class UserListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = "user/list.html"
    permission_required = "view_user"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse({"error": "Ha ocurrido un error"}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de usuarios"
        context["create_url"] = reverse_lazy("user:user_create")
        context["list_url"] = reverse_lazy("user:user_list")
        context["entity"] = "Usuarios"
        context["parent"] = "empresa"
        context["segment"] = "usuario"
        return context


class UserCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "user/create.html"
    success_url = reverse_lazy("user:user_list")
    permission_required = "add_user"
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
        context["title"] = "Creación un usuario"
        context["entity"] = "Usuarios"
        context["list_url"] = self.success_url
        context["action"] = "add"
        context["parent"] = "empresa"
        context["segment"] = "usuario"
        return context


class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "user/create.html"
    success_url = reverse_lazy("user:user_list")
    permission_required = "change_user"
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
        context["title"] = "Edición de un usuario"
        context["entity"] = "Usuarios"
        context["list_url"] = self.success_url
        context["action"] = "edit"
        context["parent"] = "empresa"
        context["segment"] = "usuario"
        return context


class UserDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = User
    template_name = "user/delete.html"
    success_url = reverse_lazy("user:user_list")
    permission_required = "delete_user"
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
        context["title"] = "Eliminación de un usuario"
        context["entity"] = "Usuarios"
        context["list_url"] = self.success_url
        context["parent"] = "empresa"
        context["segment"] = "usuario"
        return context


class UserChangeGroup(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(pk=self.kwargs["pk"])
            request.session["group_id"] = group.id
            request.session["group_name"] = group.name
        except:
            pass
        return HttpResponseRedirect(reverse_lazy("calibus:dashboard"))


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "user/profile.html"
    success_url = reverse_lazy("calibus:dashboard")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

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
        context["title"] = "Edición de perfil"
        context["entity"] = "Perfil"
        context["list_url"] = self.success_url
        context["action"] = "edit"
        context["parent"] = "empresa"
        context["segment"] = "usuario"
        return context
