from django.shortcuts import render
# Para la vista de Programs
from rest_framework import generics
from rest_framework.views import APIView
from datetime import datetime
from .models import Program
from .serializers import ProgramSerializer
from rest_framework.permissions import IsAuthenticated
# Para la creacion de programas
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
# Para vistas basadas en funciones
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
# Modelos de Usuarios
from users.models import User

# Create your views here.
class ProgramListByDateView(generics.ListAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        """Filtra los programas por la fecha recibida en el parámetro 'date'."""
        
        # Mostrar la fecha recibida con emojis
        date_str = self.request.query_params.get('date', None)
        print(f"📅 Fecha recibida: {date_str}")

        if date_str:
            try:
                # Intentamos convertir la fecha
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                print(f"✅ Formato de fecha válido: {date}")

                # Filtrar los programas por la fecha
                queryset = Program.objects.filter(start_time__date=date)
                print(f"🔍 Programas encontrados: {queryset.count()}")

                return queryset
            except ValueError:
                # Si el formato de fecha es incorrecto
                print("❌ Error en el formato de fecha")
                return Program.objects.none()  # No devolver programas si la fecha es inválida

        print("🔄 No se proporcionó una fecha, devolviendo todos los programas.")
        return Program.objects.all()
    

# @api_view(['POST'])
# def create_program(request):
#     """
#     Crea un nuevo programa con los datos recibidos en 'form-data'.
#     Los datos incluyen título, descripción, fecha y hora, categoría, imagen y el host.
#     """
#     if request.method == 'POST':
#         # Instancia del parser que maneja formularios con archivos (multipart)
#         parser_classes = [MultiPartParser, FormParser]
        
#         # Usamos el serializer para validar y guardar los datos
#         serializer = ProgramSerializer(data=request.data)
        
#         if serializer.is_valid():
#             # Guardamos el programa si los datos son válidos
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProgramCreateView(APIView):
    """
    Vista para crear un programa con autenticación basada en token y manejo de archivos (imagen).
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Asegura que solo usuarios autenticados puedan acceder a esta vista.
    parser_classes = [MultiPartParser, FormParser]  # Permite la carga de archivos.

    # Para obtener datos relacionados con los select
    def get(self, request, *args, **kwargs):
        # Extraer las categorías definidas en el modelo, agregando un id (podrías usar el value como id)
        categories = [
            {'id': choice[0], 'value': choice[0], 'label': choice[1]}
            for choice in Program.CATEGORY_CHOICES
        ]
        # Obtener la lista de usuarios disponibles
        users = User.objects.all()
        # Convertir el queryset a una lista de diccionarios formateada, usando get_full_name
        users_list = [
            {
                'id': user.id, 
                'full_name': user.get_full_name()
            }
            for user in users
        ]
        return Response({
            'categories': categories,
            'users': users_list
        }, status=status.HTTP_200_OK)
    
    # Para completar el formulario
    def post(self, request, *args, **kwargs):
        """
        Crea un programa con los datos recibidos en el 'form-data'.
        Los datos incluyen título, descripción, fecha, categoría, imagen y el host.
        """
        # Mostrar información de usuario autenticado con emojis
        print(f"✅ Usuario autenticado: {request.user.username}")
        print(f"🆔 Session ID después del login: {request.session.session_key}")

        # Mostrar los datos recibidos para debugging con emojis
        print("📥 Datos recibidos:", request.data)

        # Asignamos el usuario autenticado al campo `user_made`
        request.data['user_made'] = request.user.id  # El usuario que crea el programa

        # Creamos el serializer con los datos del request
        serializer = ProgramSerializer(data=request.data)

        # Validamos el serializer
        if serializer.is_valid():
            # Guardamos el programa si los datos son válidos
            program = serializer.save()

            # Si se ha subido una imagen, se maneja aquí automáticamente
            if 'image' in request.FILES:
                program.image = request.FILES['image']
                program.save()

            print(f"🎉 ¡Programa creado exitosamente! ID del programa: {program.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Si el serializer no es válido, devolvemos los errores con emoji
        print("❌ Error al crear el programa:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
