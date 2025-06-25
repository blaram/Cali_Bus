from django.urls import path
from core.calibus.views.route.views import *
from core.calibus.views.client.views import *
from core.calibus.views.dashboard.views import *
from core.calibus.views.travel.views import *
from core.calibus.views.parcel.views import *
from core.calibus.views.bus.views import *
from core.calibus.views.remittance.views import *
from core.calibus.views.tests.views import TestView
from core.calibus.views.ticket.views import *

app_name = "calibus"

urlpatterns = [
    # route
    path("route/list/", RouteListView.as_view(), name="route_list"),
    path("route/add/", RouteCreateView.as_view(), name="route_create"),
    path("route/update/<int:pk>/", RouteUpdateView.as_view(), name="route_update"),
    path("route/delete/<int:pk>/", RouteDeleteView.as_view(), name="route_delete"),
    # client
    path("client/list/", ClientListView.as_view(), name="client_list"),
    path("client/add/", ClientCreateView.as_view(), name="client_create"),
    path("client/update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("client/delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path(
        "client/autocomplete/",
        ClientAutocompleteView.as_view(),
        name="client_autocomplete",
    ),
    # travel
    path("travel/list/", TravelListView.as_view(), name="travel_list"),
    path("travel/add/", TravelCreateView.as_view(), name="travel_create"),
    path("travel/update/<int:pk>/", TravelUpdateView.as_view(), name="travel_update"),
    path("travel/delete/<int:pk>/", TravelDeleteView.as_view(), name="travel_delete"),
    # home
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # test
    path("test/", TestView.as_view(), name="test"),
    # parcel
    path("parcel/list/", ParcelListView.as_view(), name="parcel_list"),
    path("parcel/add/", ParcelCreateView.as_view(), name="parcel_create"),
    path("parcel/change_status/", change_status, name="parcel_change_status"),
    # bus
    path("bus/list/", BusListView.as_view(), name="bus_list"),
    path("bus/add/", BusCreateView.as_view(), name="bus_create"),
    path("bus/update/<int:pk>/", BusUpdateView.as_view(), name="bus_update"),
    path("bus/delete/<int:pk>/", BusDeleteView.as_view(), name="bus_delete"),
    # remittance
    path("remittance/list/", RemittanceListView.as_view(), name="remittance_list"),
    path("remittance/add/", RemittanceCreateView.as_view(), name="remittance_create"),
    # ticket
    path("ticket/list/", TravelSaleListView.as_view(), name="travel_sale_list"),
    path("ticket/add/", TicketCreateView.as_view(), name="ticket_create"),
    path(
        "passenger/list/pdf/<int:travel_id>/",
        PassengerListPdfView.as_view(),
        name="passenger_list_pdf",
    ),
]
