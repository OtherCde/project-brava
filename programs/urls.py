from django.urls import path
from .views import *
# Autenticacion por TOKENS
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Ruta para obtener los programas relacionados a una fecha
    path(
        '', 
        ProgramListByDateView.as_view(),
        name='login'
    ),  # Ruta para el login
    path(
        'create/',
        ProgramCreateView.as_view(),
        name='register'
    ), # Ruta para el registro
]