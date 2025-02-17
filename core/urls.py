from django.urls import path
from .views import *
# Autenticacion por TOKENS
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Ruta para obtener un usuario logeado
    path(
        'get-user/', 
        auth_status, 
        name='login'
    ),  

]