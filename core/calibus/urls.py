from django.urls import path
from core.calibus.views.role.views import role_list

app_name = 'calibus'

urlpatterns = [
    path('role/list/', role_list, name='role_list'),
]
