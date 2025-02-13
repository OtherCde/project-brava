from django import forms
from .models import User
from core.mixins import FormValidationMixin, BaseForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from django.conf import settings
import os

class LoginForm(FormValidationMixin):

    user_or_email = forms.CharField(
        label="Usuario o Email",
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.TextInput(attrs={'placeholder': "Ingrese usuario o correo", 'class': 'form-control'})        
    )
    password = forms.CharField(
        label="Contraseña",
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña', 'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['user_or_email', 'password']

    def clean_user_or_email(self):
        user_or_email = self.cleaned_data.get("user_or_email")
        
        # Verificar si el campo está vacío
        if not user_or_email:
            raise forms.ValidationError("Este campo es obligatorio.")
        
        # Verificar si es un correo o un nombre de usuario
        if "@" in user_or_email:
            # Validar si el correo está registrado
            if not User.objects.filter(email=user_or_email).exists():
                raise forms.ValidationError("El email no está registrado.")
        else:
            # Validar si el nombre de usuario está registrado
            if not User.objects.filter(username=user_or_email).exists():
                raise forms.ValidationError("El nombre de usuario no está registrado.")
        
        return user_or_email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        self.validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        user_or_email = cleaned_data.get("user_or_email")
        password = cleaned_data.get("password")
        
        # Verificar que el campo no esté vacío
        if not user_or_email or not password:
            raise forms.ValidationError("Por favor, complete todos los campos.")

        return cleaned_data

# Formulario de registro
class RegisterForm(FormValidationMixin):
    username = forms.CharField(
        label="Nombre de usuario", 
        required=True, 
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.TextInput(attrs={'placeholder': "Ingrese su nombre de usuario", 'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="Nombre", 
        required=True, 
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.TextInput(attrs={'placeholder': "Ingrese su nombre", 'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Apellido", 
        required=True, 
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.TextInput(attrs={'placeholder': "Ingrese su apellido", 'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Correo electrónico", 
        required=True, 
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.EmailInput(attrs={'placeholder': "Ingrese su correo", 'class': 'form-control'})  # Usa EmailInput aquí
    )
    password = forms.CharField(
        label="Contraseña", 
        required=True, 
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.PasswordInput(attrs={'placeholder': "Ingrese su contraseña", 'class': "form-control"})
    )
    password_confirm = forms.CharField(
        label="Confirmar contraseña", 
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'}, 
        widget=forms.PasswordInput(attrs={'placeholder': "Confirme su contraseña", 'class': "form-control"})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        self.validate_username(username)  # Llamada al mixin para validar el usuario
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        self.validate_name(first_name)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        self.validate_name(last_name)
        return last_name
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        self.validate_password(password)
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        self.validate_email(email)  # Llamada al mixin para validar el email
        return email

    def clean(self):
        cleaned_data = super().clean()
        self.validate_not_empty_fields(cleaned_data)  # Validación de campos no vacíos
        error_messages={'required': 'Este campo es obligatorio.'}
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden.")

        self.validate_not_empty_fields(cleaned_data)  # Validación personalizada
        return cleaned_data




class ProfileForm(BaseForm, FormValidationMixin):
    profile_image = forms.ImageField(
        label="Imagen de perfil",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control mb-1',
            'id': 'profileImageUpload',
        })
    )

    username = forms.CharField(
        label="Nombre de Usuario",
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.TextInput(
            attrs={
                
                'class': 'form-control mb-1'
            }
        )
    )

    first_name = forms.CharField(
        label="Nombre",
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.TextInput(
            attrs={
                
                'class': 'form-control mb-1'
            }
        )
    )

    last_name = forms.CharField(
        label="Apellido",
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.TextInput(
            attrs={
            
                'class': 'form-control mb-1'
            }
        )
    )

    email = forms.CharField(
        label="Email",
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'},
        widget=forms.TextInput(
            attrs={
                
                'class': 'form-control mb-1'
            }      
        )
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_image']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        # Establece la carpeta de imágenes en static/imgs
        image_folder = os.path.join(settings.STATICFILES_DIRS[0], 'imgs')
        
        # Cargar las imágenes disponibles en la carpeta si existe
        available_images = os.listdir(image_folder) if os.path.exists(image_folder) else []
        
        # Definir las opciones para el campo profile_image
        self.fields['profile_image'].choices = [
            (f'imgs/{image}', image) for image in available_images
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        self.validate_username(username)  # Llamada al mixin para validar el usuario
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        self.validate_name(first_name)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        self.validate_name(last_name)
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        self.validate_email_structure(email)  # Llamada al mixin para validar la estructura del email email
        return email

    def clean(self):
        cleaned_data = super().clean()
        self.validate_not_empty_fields(cleaned_data)  # Validación de campos no vacíos
        error_messages={'required': 'Este campo es obligatorio.'}
        return cleaned_data

    def get_errors_as_dict(self):
        return {field: error.get_json_data() for field, error in self.errors.items()}
    

    # Formulario para Usuarios

class UserForm(UserCreationForm):
    """
    Formulario para crear o actualizar un usuario, incluyendo la asignación de grupos.
    """
    username = forms.CharField(
        required=True,
        label="Nombre de Usuario",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de usuario.'
            }
        )
    )
    first_name = forms.CharField(
        required=True,
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del usuario.'
            }
        )
    )
    last_name = forms.CharField(
        required=True,
        label="Apellido",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido del usuario.'
            }
        )
    )
    email = forms.EmailField(
        required=True,
        label="Correo Electrónico",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el correo electrónico.'
            }
        )
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una contraseña.'
            }
        )
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirme la contraseña.'
            }
        )
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Grupos de Usuarios",
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control js-user-multiple',
            }
        )
    )
    is_active = forms.BooleanField(
        required=False,
        label="¿Está activo?",
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
            }
        )
    )
    is_staff = forms.BooleanField(
        required=False,
        label="¿Es personal administrativo?",
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password_custom')
        password2 = cleaned_data.get('password_custom2')
        # Verificar que las contraseñas coinciden
        if password and password2 and password != password2:
            raise ValidationError('Las contraseñas no coinciden.')
        # Establecer la contraseña encriptada
        user = self.instance
        if password:
            user.set_password(password)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        self.save_m2m()  # Guardar las relaciones ManyToMany
        return user
