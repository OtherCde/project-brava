from django.urls import path
from .views import *

urlpatterns = [
    # Vista para recuperar todas las publicidades vigentes
    path(
        '', 
        AdvertisementListView.as_view(), 
        name='advertisement-list'
    ),
]
