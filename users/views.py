from django.shortcuts import get_object_or_404, render, redirect
# Autenticacion de DJANGO
from django.contrib.auth import authenticate, login
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.middleware.csrf import get_token
# Messages
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q, F
from .forms import LoginForm, RegisterForm, ProfileForm, UserForm
from .models import User
from django.http import JsonResponse  # Asegúrate de importar JsonResponse
from django.contrib.auth import logout  # Importa logout para terminar la sesión
from django.views.decorators.csrf import csrf_exempt  # Importa csrf_exempt solo si es necesario
# Utilidades
from core.utils import is_ajax
# Para la API
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Para obtener datos del USUARIO LOGEADO
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
# TOKEN
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print("Datos recibidos:", request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            remember = serializer.validated_data['remember']

            # 🔥 Autenticar al usuario para asegurarnos de que Django lo reconoce
            user1 = authenticate(request, username=user.username, password=request.data.get("password"))

            if user1 is None:
                return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

            login(request, user)  # 🔥 Iniciar sesión en Django

            # 🔥 Asegurar que la sesión se guarde correctamente
            request.session.modified = True  
            request.session.save()

            # 🔥 Forzar a Django a reconocer la sesión
            AuthenticationMiddleware(lambda req: None)(request)

            print(f"✅ Usuario autenticado: {user1.username}")
            print(f"🆔 Session ID después del login: {request.session.session_key}")


            if remember:
                request.session.set_expiry(1209600)  # 2 semanas
            else:
                request.session.set_expiry(0)  # Expira al cerrar el navegador

            # Generar el token utilizando SimpleJWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Inicio de sesión exitoso',
                'token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user_or_email = form.cleaned_data.get('user_or_email')
#             password = form.cleaned_data.get('password')
#             remember = request.POST.get('remember') or None

#             # Intentar autenticar como nombre de usuario
#             user = authenticate(request, username=user_or_email, password=password)
#             if user is None:
#                 # Intentar autenticar como email
#                 try:
#                     user_obj = User.objects.get(email=user_or_email)
#                     user = authenticate(request, username=user_obj.username, password=password)
#                 except User.DoesNotExist:
#                     user = None

#             if user is not None:
#                 # Manejar "Recuérdame"
#                 if remember:
#                     request.session.set_expiry(1209600)  # 2 semanas
#                 else:
#                     request.session.set_expiry(0)  # Expira al cerrar el navegador
#                 login(request, user)

#                 # Almacenar el nombre del usuario en la sesión para usarlo en la barra superior
#                 request.session['username'] = user.username
#                 return redirect('core_app:home')
#             else:
#                 # Usuario o contraseña incorrectos
#                 messages.error(request, 'Usuario o contraseña incorrectos.')
#         else:
#             print("Errores del formulario:", form.errors)
#     else:
#         form = LoginForm()
#     return render(request, 'home/login.html', {'form': form})

# USER LOGIN
class UserProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retorna el usuario autenticado."""
        return self.request.user

# REGISTER
# Vista BASADA EN CLASE con REST_FRAMEWORK
class RegisterView(APIView):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Usuario registrado correctaente",
                    "user": UserSerializer(user).data # Devolevmos los datos del usuario registrado
                },
                status=status.HTTP_201_CREATED
            )
        # SI LA PETICION ES FALSA
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Vista BASADA EN FUNCION con DJANGO
# def register_view(request):
#     if request.method == 'POST':
#         print(request.POST)
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])  # Establecer la contraseña encriptada
#             user.save()
#             messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
#             return redirect('users_app:login')  # Redirige a la página de inicio de sesión
#         else:
#             messages.error(request, 'Error al registrar. Verifica los datos ingresados.')
#     else:
#         form = RegisterForm()

#     return render(request, 'home/register.html', {'form': form})



# LOGOUT
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden cerrar sesión

    def post(self, request):
        # Si usas JWT, revoca el token
        if 'refresh_token' in request.data:
            try:
                refresh = RefreshToken(request.data['refresh_token'])
                refresh.blacklist()  # Solo si usas Django REST Framework SimpleJWT con blacklist habilitado
            except Exception:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        # Para autenticación con sesión
        logout(request)

        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
    
    
# @csrf_exempt # Solo si estás usando fetch sin un formulario, para evitar problemas con CSRF
# def logout_view(request):
#     # Validamos que la peticion sea POST
#     if request.method == 'POST':  # Solo permitimos POST para mayor seguridad
#         logout(request)
#         return JsonResponse({'status': 'success', 'message': 'User logged out successfully'})
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# @login_required
# def profile_edit_view(request):
#     user = request.user

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=user)  # Agregar request.FILES para manejar archivos
#         if form.is_valid():
#             # Guardar los cambios del formulario en la base de datos
#             user = form.save(commit=False)

#             # Si hay una imagen de perfil seleccionada o subida, actualizarla
#             selected_image = form.cleaned_data.get('profile_image')
#             if selected_image:
#                 user.profile_image = selected_image  # Asumiendo que el modelo tiene un campo `profile_image`

#             user.save()  # Guarda los cambios del usuario, incluidos los datos actualizados

#             # Guardar la imagen de perfil seleccionada en la sesión para mostrarla después
#             request.session['profile_image'] = selected_image

#             messages.success(request, 'Perfil actualizado exitosamente.')
#             return redirect('users_app:profile')  # Asegúrate de que esta vista redirija a la página principal o a donde desees
#         else:
#             messages.error(request, 'Hubo un error al actualizar el perfil.')
#     else:
#         form = ProfileForm(instance=user)
#         # Asigna la imagen seleccionada previamente, si existe
#         form.initial['profile_image'] = request.session.get('profile_image', 'default.png')

#     context = {
#         'form': form,
#     }

#     return render(request, 'home/page-user.html', context)



# # USERS

# # Create your views here.
# def user_list(request):
#     """
#     Método que redirecciona al datatable de usuarios.
#     """
#     urls = [
#         {'id': 'user_create', 'name': 'users_app:users_create'},
#         {'id': 'user_edit', 'name': 'users_app:users_update'},
#         {'id': 'user_detail', 'name': 'users_app:users_detail'},
#         {'id': 'user_delete', 'name': 'users_app:users_delete'}
#     ]
#     exclude_fields = ['user_made', 'deleted_at', 'created_at', 'updated_at', 'comments']
#     context = {
#         'url_datatable': reverse('users_app:users-datatable'),
#         'user_form': ProfileForm(),
#         'urls': urls,
#         'segment': 'page-user',
#     }

#     return render(request, "users/users_page.html", context)

# def UsersAjaxList(request):
#     draw = request.GET.get('draw')
#     start = int(request.GET.get('start', 0))
#     length = int(request.GET.get('length', 10))

#     order_column_index = int(request.GET.get('order[0][column]', 0))
#     order_direction = request.GET.get('order[0][dir]', 'asc')
#     search_value = request.GET.get('search[value]', None)

#     column_mapping = { 
#         0: 'id',
#         1: 'username',
#         2: 'email', 
#         3: 'is_active'
#     } 
    
#     order_column = column_mapping.get(order_column_index, 'id')
    
#     if order_direction == 'asc':
#         order_column = F(order_column).asc(nulls_last=True)
#     else:
#         order_column = F(order_column).desc(nulls_last=True)

#     conditions = Q()
#     if search_value:
#         fields = ['username', 'email', 'first_name', 'last_name', 'id']
#         search_terms = search_value.split()

#         for term in search_terms:
#             term_conditions = Q()
#             for field in fields:
#                 term_conditions |= Q(**{f"{field}__icontains": term})
#             conditions &= term_conditions

#     filtered_data = User.objects.filter(conditions) if conditions else User.objects.all()
#     filtered_data = filtered_data.distinct().order_by(order_column)
#     total_records = filtered_data.count()

#     data = [item.to_json() for item in filtered_data[start: start + length]]
    
#     return JsonResponse(
#         {
#             'draw': draw,
#             'recordsTotal': total_records,
#             'recordsFiltered': total_records,
#             'data': data,
#         }
#     )

# def create_user(request):
#     """
#     Vista para crear un nuevo usuario
#     """
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()  # Guardar el nuevo usuario
#             messages.success(request, "Usuario creado exitosamente.")
#             return redirect('users_app:list')
#         else:
#             messages.error(request, "Por favor, corrige los errores.")
#             print(f"Errores en CREATE USER: {form.errors}")
#     else:
#         form = UserForm()  # Formulario vacío para la primera carga

#     context = {
#         'form': form,
#     }

#     return render(request, 'users/user_form.html', context)

# def detail_user(request, pk):
#     """
#     Vista que me permite ver el detalle de un usuario.
#     """
#     try:
#         user = get_object_or_404(User, pk=pk)
#         if is_ajax(request):
#             data = user.to_json()
#             object = {
#                 'status': 'success',
#                 'user': data
#             }
#             return JsonResponse(object, status=200)
        
#         print("NO ES UNA PETICIÓN AJAX")
#         return JsonResponse({'status': 'error', 'message': 'La solicitud no es AJAX.'}, status=400)
#     except Exception as e:
#         print(f"Error back --> {str(e)}")
#         # En caso de error, retorna un JSON con el estado de error
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# def update_user(request, pk):
#     """
#     Vista para actualizar un usuario existente.
#     """
#     user = get_object_or_404(User, pk=pk)

#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Usuario actualizado exitosamente.")
#             return redirect('users_app:user_list')
#         else:
#             messages.error(request, "Por favor, corrige los errores.")
#             print(f"Errores en UPDATE USER: {form.errors}")
#     else:
#         form = UserForm(instance=user)  # Cargar el formulario con los datos actuales del usuario

#     context = {
#         'form': form,
#         'user': user,
#     }

#     return render(request, 'users/user_form.html', context)

# def delete_user(request, pk):
#     """
#     Vista que me permite eliminar un usuario.
#     """
#     try:
#         if request.method == 'POST':
#             user = get_object_or_404(User, pk=pk)
#             user.delete()
#             if is_ajax(request):
                
#                 data = user.to_json()
#                 context = {
#                     'status': 'success',
#                     'message': 'Usuario eliminado con exito',
#                     'user': data
#                 }
#                 # No agregamos messages.success porque al ser una eliminacion dinamica no suele pasar el mensaje a menos que se actualice
#                 return JsonResponse(context, status=200)
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'La solicitud no es AJAX.'}, status=400)
        

#     except Exception as e:
#         print(f"Error back --> {str(e)}")
#         # En caso de error, retorna un JSON con el estado de error
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


############################################################
####################### AUTENTICACION POR GOOGLE ######################
############################################################
from django.conf import settings
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.core.files.base import ContentFile
import re
import requests
import json

User = get_user_model()

class GoogleLogin(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            code = data.get("code")

            if not code:
                return Response({"error": "Código de autorización no proporcionado"}, status=400)

            # 🔥 Intercambiar `code` por un `id_token`
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": "https://fmbravasalta.com.ar/",  # Asegúrate de que coincide con Google Console
                "grant_type": "authorization_code",
            }

            token_response = requests.post(token_url, data=token_data)
            token_json = token_response.json()

            # print("Respuesta de Google:", token_json)  # 🔎 Depuración

            if "id_token" not in token_json:
                return Response({"error": "No se pudo obtener el ID Token"}, status=400)

            id_token_google = token_json["id_token"]

            # 🔥 Verificar ID Token con Google
            id_info = id_token.verify_oauth2_token(
                id_token_google,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            # print("Datos del token:", id_info)

            # Verificar audiencia y issuer
            if id_info["aud"] != settings.GOOGLE_CLIENT_ID:
                raise ValueError("El token no está destinado a este cliente.")

            if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
                raise ValueError("Issuer incorrecto.")

            # Obtener información del usuario
            email = id_info["email"]
            first_name = id_info.get("given_name", "")
            last_name = id_info.get("family_name", "")
            profile_picture_url = id_info.get("picture", "")  # 🔥 Obtener la imagen de perfil

            # Generar username único
            username = re.sub(r"[^a-zA-Z0-9_]", "", email.split("@")[0])
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # Crear o obtener usuario
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )

            # 🔥 Si el usuario es nuevo, descargar la imagen y guardarla
            if created and profile_picture_url:
                response = requests.get(profile_picture_url, stream=True)
                if response.status_code == 200:
                    file_name = f"profile_{user.username}.jpg"

                    # Guarda la imagen correctamente en Django
                    user.set_unusable_password()  # Marca al usuario como que no tiene con
                    user.profile_image.save(
                        file_name,
                        ContentFile(response.content),  # Asegura que se almacena el contenido, no la URL
                        save=True
                    )

            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                }
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            print("Error durante la validación del token:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error general:", str(e))
            return Response({"error": "Error en el servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
############################################################
####################### AUTENTICACION POR FACEBOOK ######################
############################################################

class FacebookLogin(APIView):
    def post(self, request):
        try:
            # Usamos "access_token" o "code" (en este caso, el frontend envía el access token en la propiedad 'code')
            token = request.data.get('access_token') or request.data.get('code')
            # print("Token recibido desde el frontend:", token)
            
            if not token:
                return Response({"error": "Token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

            # Como ya se tiene un access token, lo usaremos directamente.
            access_token = token
            # print("Usando access token recibido:", access_token)

            # 1. Obtener datos del usuario directamente usando el access token
            graph_url = "https://graph.facebook.com/me"
            graph_params = {
                "fields": "id,email,first_name,last_name,picture",
                "access_token": access_token
            }
            
            # print("Solicitando datos del usuario a Facebook con el access token...")
            user_response = requests.get(graph_url, params=graph_params)
            user_data = user_response.json()
            print("Datos del usuario obtenidos:", user_data)

            # Obtener imagen de perfil
            profile_picture_url = user_data.get("picture", {}).get("data", {}).get("url", "")
            
            if 'email' not in user_data:
                return Response({"error": "Email no proporcionado por Facebook"}, status=status.HTTP_400_BAD_REQUEST)

            # 2. Procesar la información del usuario
            email = user_data['email']
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            # print("Procesando usuario - Email:", email, "First Name:", first_name, "Last Name:", last_name)
            
            # Generar username único
            username = email.split('@')[0]
            base_username = re.sub(r'[^a-zA-Z0-9_]', '', username)
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            # print("Username final generado:", username)

            # 3. Crear o obtener usuario
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            
            # Si el usuario es nuevo, descargar y guardar la imagen de perfil
            if created and profile_picture_url:
                try:
                    response = requests.get(profile_picture_url, stream=True)
                    if response.status_code == 200:
                        file_name = f"profile_{user.username}.jpg"
                        user.profile_image.save(
                            file_name,
                            ContentFile(response.content),  # Asegura que se almacena el contenido, no la URL
                            save=True
                        )
                except Exception as e:
                    print(f"Error al guardar la imagen de perfil: {str(e)}")
                    # Si no se puede obtener la imagen, puedes establecer una imagen predeterminada
                    user.profile_image = 'media/default.svg'
                    user.save()

            # Si el usuario es nuevo, también establecemos una contraseña inválida
            if created:
                user.set_unusable_password()
                user.save()

            # 4. Generar JWT
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                }
            }
            print("Respuesta final con tokens JWT:", response_data)
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print("Error en Facebook Login:", str(e))
            return Response({"error": "Error en el servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)