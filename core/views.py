from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Para inicio de sesion con Google y Facebook
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.serializers import JWTSerializer

# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])  # 🔥 Protege la vista con autenticación
def auth_status(request):
    return Response({
        "isAuthenticated": True,
        "username": request.user.username
    })

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = JWTSerializer  # Para usar JWT

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = JWTSerializer  # Para usar JWT