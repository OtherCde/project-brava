from django.urls import path
from .views import *
# Autenticacion por TOKENS
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path(
        'login/', 
        LoginView.as_view(), 
        name='login'
    ),  # Ruta para el login
    path(
        'register/', 
        RegisterView.as_view(), 
        name='register'
    ), # Ruta para el registro
    path(
        'logout/',
        LogoutView.as_view(),
        name="logout"
    ),
    # Ruta para obtener el usuario logeado
    path(
        'profile/',
        UserProfileView.as_view(),
        name="profile"
    ),
    # Ruta para crear usuarios
    # path(
    #     'create/',
    #     create_user,
    #     name="users_create"
    # ),
    # path(
    #     'update/<int:pk>/',
    #     update_user,
    #     name="users_update"
    # ),
    # path(
    #     'detail/<int:pk>/',
    #     detail_user,
    #     name="users_detail"
    # ),
    # path(
    #     'delete/<int:pk>/',
    #     delete_user,
    #     name="users_delete"
    # ),
    # Tokens
    path(
        'token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair'
    ),  # Obtener token
    path(
        'token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'
    ),  # Refrescar token
    # Login con GOOGLE
    path(
        'login/google/',
        GoogleLogin.as_view(),
        name="google_login"
    ),
    # Login con FACEBOOK
    path(
        'login/facebook/',
        FacebookLogin.as_view(),
        name="facebook_login"
    ),
]