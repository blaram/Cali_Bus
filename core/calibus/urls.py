from django.urls import path
from core.calibus.views.role.views import *
from core.calibus.views.dashboard.views import *

app_name = 'calibus'

urlpatterns = [
    path('role/list/', RoleListView.as_view(), name='role_list'),
    path('role/add/', RoleCreateView.as_view(), name='role_create'),
    path('role/update/<int:pk>/', RoleUpdateView.as_view(), name='role_update'),
    path('role/delete/<int:pk>/', RoleDeleteView.as_view(), name='role_delete'),
    path('role/form/', RoleFormView.as_view(), name='role_form'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
