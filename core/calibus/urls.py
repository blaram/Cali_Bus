from django.urls import path
from core.calibus.views.route.views import *
from core.calibus.views.client.views import *
from core.calibus.views.dashboard.views import *
from core.calibus.views.travel.views import *
from core.calibus.views.tests.views import TestView

app_name = 'calibus'

urlpatterns = [
    # route
    path('route/list/', RouteListView.as_view(), name='route_list'),
    path('route/add/', RouteCreateView.as_view(), name='route_create'),
    path('route/update/<int:pk>/', RouteUpdateView.as_view(), name='route_update'),
    path('route/delete/<int:pk>/', RouteDeleteView.as_view(), name='route_delete'),
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/',
         ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/',
         ClientDeleteView.as_view(), name='client_delete'),
    # travel
    path('travel/list/', TravelListView.as_view(), name='travel_list'),
    path('travel/add/', TravelCreateView.as_view(), name='travel_create'),
    path('travel/update/<int:pk>/',
         TravelUpdateView.as_view(), name='travel_update'),
    path('travel/delete/<int:pk>/',
         TravelDeleteView.as_view(), name='travel_delete'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # test
    path('test/', TestView.as_view(), name='test'),
]
