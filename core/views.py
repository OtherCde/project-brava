from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])  # 🔥 Protege la vista con autenticación
def auth_status(request):
    return Response({
        "isAuthenticated": True,
        "username": request.user.username
    })