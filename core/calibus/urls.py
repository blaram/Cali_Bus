from django.urls import path
from core.calibus.views.role.views import *
from core.calibus.views.dashboard.views import *
from core.calibus.views.bus.views import *

app_name = 'calibus'

urlpatterns = [
    # role
    path('role/list/', RoleListView.as_view(), name='role_list'),
    path('role/add/', RoleCreateView.as_view(), name='role_create'),
    path('role/update/<int:pk>/', RoleUpdateView.as_view(), name='role_update'),
    path('role/delete/<int:pk>/', RoleDeleteView.as_view(), name='role_delete'),
    path('role/form/', RoleFormView.as_view(), name='role_form'),
    # bus
    path('bus/list/', BusListView.as_view(), name='bus_list'),
    path('bus/add/', BusCreateView.as_view(), name='bus_create'),
    path('bus/update/<int:pk>/', BusUpdateView.as_view(), name='bus_update'),
    path('bus/delete/<int:pk>/', BusDeleteView.as_view(), name='bus_delete'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
