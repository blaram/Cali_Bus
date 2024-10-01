from django.urls import path
from core.calibus.views.role.views import *

app_name = 'calibus'

urlpatterns = [
    path('role/list/', RoleListView.as_view(), name='role_list'),
]
