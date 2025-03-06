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
    # Autenticacion por google
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    # Autenticacion por Facebook
    path('auth/facebook/', FacebookLogin.as_view(), name='facebook_login'),

]