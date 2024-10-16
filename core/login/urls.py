from django.urls import path
from core.login.views import *

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
]
