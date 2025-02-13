from django.shortcuts import  redirect, render
from django.http import JsonResponse
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

# Create here utils 

def getColumnsForModel(model, exclude_fields=None,include_fields=None):
    """
    Devuelve una lista con los verbose_name de los campos de la tabla para un modelo Django, excluyendo los campos especificos.
    Args:
        model (Model): Clase de modelo Django
        exclude_fields (list, optional): Lista de nombres de campos a excluir. Por defecto es None

    Returns:
        list: Lista con los verbose_name de los campos de la tabla
    """
    if exclude_fields is None:
        exclude_fields = []
    if include_fields is None:
        include_fields = []

    if include_fields:
        if exclude_fields:
            return [field.verbose_name for field in model._meta.get_fields()
                    if field.concrete and hasattr(field, 'verbose_name') and 
                    field.name in include_fields and field.name not in exclude_fields]
        else:
            return [field.verbose_name for field in model._meta.get_fields()
                    if field.concrete and hasattr(field, 'verbose_name') and field.name in include_fields]
    elif exclude_fields:
        return [field.verbose_name for field in model._meta.get_fields()
                if field.concrete and hasattr(field, 'verbose_name') and field.name not in exclude_fields]
    else:
        return [field.verbose_name for field in model._meta.get_fields()
                if field.concrete and hasattr(field, 'verbose_name')]

def is_ajax(request):
    """
    Para saber si es una peticion AJAX
    request: Como parametro para saber el tipo de peticion
    return bool -> V si es una peticion AJAX -> F si no es una peticion AJAX
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

User = get_user_model()

def validate_username_length(username, min_length=5):
    if len(username) < min_length or not username.isalpha():
        raise ValidationError(f"El nombre de usuario debe tener al menos {min_length} caracteres alfabéticos.")

def validate_email_not_registered(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError("El correo ya está registrado.")

def validate_username_not_registered(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError("El nombre de usuario ya está registrado.")

def validate_email_structure(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        raise ValidationError("El email no tiene una estructura válida.")

def validate_name_is_alpha(value):
    # Código de validación para asegurar que el nombre solo contenga caracteres alfabéticos
    if not value.isalpha():
        raise ValidationError("El nombre solo debe contener caracteres alfabéticos.")

def validate_password_length(password, min_length=6):
    if len(password) < min_length:
        raise ValidationError(f"La contraseña debe tener al menos {min_length} caracteres.")
    
def validate_email_exists(email):
    if not User.objects.filter(email=email).exists():
        raise ValidationError("El email no está registrado.")