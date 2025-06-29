from django.urls import path
from core.user.views import *


app_name = "user"

urlpatterns = [
    # user
    path("list/", UserListView.as_view(), name="user_list"),
    path("add/", UserCreateView.as_view(), name="user_create"),
    # path("route/update/<int:pk>/", RouteUpdateView.as_view(), name="route_update"),
    # path("route/delete/<int:pk>/", RouteDeleteView.as_view(), name="route_delete"),
]
