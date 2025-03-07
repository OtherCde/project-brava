from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

# Obtenemos el model del Usuario
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    user_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    remember = serializers.BooleanField(default=False)

    def validate(self, data):
        user_or_email = data.get('user_or_email')
        password = data.get('password')

        user = authenticate(username=user_or_email, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=user_or_email)
                if user_obj.check_password(password):  # Verifica la contraseña manualmente
                    user = user_obj
            except User.DoesNotExist:
                user = None

        if user is None:
            raise serializers.ValidationError({"error": "Usuario o contraseña incorrectos."})

        if not user.is_active:
            raise serializers.ValidationError({"error": "Este usuario está inactivo."})

        data['user'] = user
        return data
    

# Clase para Cerrar Session    
class LogoutSerializer(serializers.Serializer):
    """
    Clase para la vista del logout
    """
    refresh_token = serializers.CharField(required=False)

    def validate(self, data):
        """
        Si se usa JWT, se puede validar y revocar el refresh token aquí.
        """
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Clase para obtener el usuario logeado
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_image']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Clase para registrar un usuario
    """
    password_confirm = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'profile_image', 'first_name', 'last_name', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},  # Evita que la contraseña se devuelva en la respuesta
        }

    def validate(self, data):
        """Verifica si las contraseñas coinciden"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        """Elimina el campo password_confirm y crea el usuario"""
        validated_data.pop('password_confirm')  # Elimina el campo antes de guardar
        user = User.objects.create_user(**validated_data)
        return user