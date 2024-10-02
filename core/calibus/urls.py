from django.urls import path
from core.calibus.views.role.views import *

app_name = 'calibus'

urlpatterns = [
    path('role/list/', RoleListView.as_view(), name='role_list'),
    path('role/list2/', role_list, name='role_list2'),
    path('role/add/', RoleCreateView.as_view(), name='role_create'),
]
