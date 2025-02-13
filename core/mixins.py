from django.shortcuts import render
from datetime import timedelta
from django.core.exceptions import ValidationError
import decimal
from django.utils import timezone
from django import forms
from .utils import (
    validate_username_length,
    validate_email_not_registered,
    validate_username_not_registered,
    validate_email_structure,
    validate_name_is_alpha,
    validate_password_length,
    validate_email_exists

)

now_local = timezone.localtime(timezone.now())
today = now_local.date()

# Clase base para formularios
class BaseForm(forms.ModelForm):
    """
    Esta clase BaseForm hereda de ModelForm
    """
    class Meta:
        abstract = True

    def get_errors_as_dict(self) -> dict:
        """
        Método que nos permitirá saber con más exactitud en qué campo del modelo está el error.
        Las claves son los FIELDS y los valores son los MENSAJES DE ERROR.
        """
        errors_dict = {}
        for field_name, errors in self.errors.items():
            errors_dict[field_name] = errors.as_text()
        return errors_dict


# Mixin de validación de formularios
class FormValidationMixin(BaseForm):

    def validate_username(self, username):
        validate_username_length(username)
        validate_username_not_registered(username)

    def validate_email(self, email):
        validate_email_not_registered(email)

    def validate_email_structure(self, email):
        validate_email_structure(email)

    def validate_not_empty_fields(self, cleaned_data):
        for field, value in cleaned_data.items():
            if not value:
                self.add_error(field, "Este campo no puede estar vacío.")

    def validate_name(self, name):
        validate_name_is_alpha(name)

    def validate_password(self, password):
        validate_password_length(password)

    def validate_email_exists(self, email):
        validate_email_exists(email)

"""Implementacion de metodos Abstractos que nos serviran para reutilizar codigo."""
class BaseForm(forms.ModelForm):
    """
    Esta clase BaseForm hereda de ModelForm
    """
    class Meta:
        abstract = True

    def get_errors_as_dict(self) -> dict:
        """
        Metodo que nos permitira saber con mas exatitud en que campo del modelo esta el error.
        Para tener en cuenta {}, las keys son los FIELDS y los value son MENSAJES DE ERROR
        return -> Devuelve un diccionario donde contiene errores de validacion del formulario.
        """
        errors_dict = {}
        print(self.errors.items())
        for field_name, errors in self.errors.items():
            errors_dict[field_name] = errors.as_text()
        return errors_dict
    
class ValidationFormMixin(BaseForm):
    """
    Esta clase extiende directamente de BaseForm y lo que tiene es validacion de codigo,
    validacion de longitud (para cadenas), validacion de fecha de nacimiento,
    validacion de numeros positivos, validacion de dni, etc
    """
    def validate_code(self, model, code, min_length, error_message):
        """
        Valida longitud del codigo y evita su replica.
        """
        if code:
            code_str = str(code)
            if len(code_str) < min_length:
                raise forms.ValidationError(error_message)
            
            # Con esta linea de codigo verificamos si estamos editando
            if hasattr(self, 'instance') and self.instance.pk:
                if model.objects.exclude(pk=self.instance.pk).filter(barcode=code_str).exists():
                    raise forms.ValidationError("El código ingresado ya está en uso.")
            else:
                # Si no pasa eso estamos creando, por lo cual verificamos si el codigo ya está en uso
                if model.objects.filter(barcode=code_str).exists():
                    raise forms.ValidationError("El código ingresado ya está en uso.")

    def validate_email(self, email):
        import re
        """
        Valida el formato del correo electronico
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, email):
            return True
        else:
            return False

    def validate_length(self, field_value, min_length, error_message):
        """
        Valida longitud de una cadena.
            Para nombres, apellidos, direcciones, telefonos, etc.
            Muestra el error mandado por argumento.
        """
        if field_value:
            field_value = str(field_value)
            if len(field_value) < min_length:
                raise forms.ValidationError(error_message)

    def validate_birth_date(self, birth_date):
        """
        Valida fecha de nacimiento.
            Debe tener por lo menos 3 meses de vida o no superar los 85 años.
        """
        if birth_date :
            if birth_date >= today - timedelta(days=2*365):
                raise forms.ValidationError('La fecha establecida no puede registrarse.')
        
    def validate_date(self, date):
        """
        Valida que la fecha ingresada no sea el mismo dia
        """
        if date:
            if date == today:
                raise forms.ValidationError('La fecha establecida no puede registrarse.')
        else:
            raise forms.ValidationError('Este campo es nesesario.')
        
    @staticmethod
    def validate_positive_integer(value, required=True):
        print("Valor",value)
        if required: 
            if not value :
                print("Este campo no puede ser nulo.")
                raise ValidationError("Este campo no puede ser nulo.")
            
        
        if value :
            try:
                value = int(value)
                if value < 0:
                    print("El valor debe ser un número entero positivo.")
                    raise ValidationError("El valor debe ser un número entero positivo.")
            except (TypeError, ValueError):
                print("El valor debe ser un número entero.")
                raise ValidationError("El valor debe ser un número entero.")
        return value


    @staticmethod
    def validate_positive_float(value, required=True):
        print("Valor", value)
        if required and (value is None or value == ''):
            raise ValidationError("Este campo no puede ser nulo.")

        if value is not None and value != '':
            try:
                value = decimal.Decimal(value)
                if value < 0:
                    print("El valor debe ser un número decimal positivo.")
                    raise ValidationError("El valor debe ser un número decimal positivo.")
                # Verificar que el número tiene hasta dos decimales
                if value.as_tuple().exponent < -2:
                    raise ValidationError("El valor no debe tener más de dos dígitos decimales.")
            except (TypeError, ValueError, decimal.InvalidOperation):
                print("El valor debe ser un número decimal.")
                raise ValidationError("El valor debe ser un número decimal.")
        return value

    def validate_percentage(self, value, min_value=None, max_value=None, required=True):
        """
        Valida que el valor del porcentaje cumpla con los criterios especificados.
        - required: Indica si el campo es obligatorio. Por defecto es True.
        - min_value: Valor mínimo permitido para el porcentaje. Opcional.
        - max_value: Valor máximo permitido para el porcentaje. Opcional.
        """
        print("Validando porcentaje:", value)
        if required and not value:
            raise ValidationError("Este campo no puede ser nulo.")
        
        if value:
            try:
                value = decimal.Decimal(value)
                if value < 0:
                    raise ValidationError("El valor debe ser un número decimal positivo.")
                
                if min_value is not None:
                    if value < min_value:
                        raise ValidationError(f"El valor debe ser mayor o igual a {min_value}.")
                    if min_value > 0:
                        self.validate_positive_float(value,required)
                
                if max_value is not None and value > max_value:
                    raise ValidationError(f"El valor debe ser menor o igual a {max_value}.")

                # Verificar que el número tiene hasta dos decimales
                if value.as_tuple().exponent < -2:
                    raise ValidationError("El valor no debe tener más de dos dígitos decimales.")
            except (TypeError, ValueError, decimal.InvalidOperation):
                raise ValidationError("El valor debe ser un número decimal.")

        return value

    def validate_dni(self, dni):
        """
        Valida el dni ingresado
        """
        import re
        dni_str = str(dni)
        if dni and (7 < len(dni_str) <= 13):
            try:
                # Eliminar puntos y espacios
                documento = re.sub(r'\.|\s', '', dni_str)
                
                # Permitir guiones en CUIT
                documento = re.sub(r'-', '', documento)

                # Verificar que la cadena resultante contenga solo dígitos y hasta 2 letras,
                # o tenga el formato CUIL/CUIT (11 dígitos seguido opcionalmente por una letra)
                if not re.match(r'^\d{0,8}[A-Za-z]{0,2}$', documento) and not re.match(r'^\d{11}[A-Za-z]?$', documento):
                    raise forms.ValidationError(f'El DNI/CUIL/CUIT ingresado solo puede contener 8 digitos (DNI) u 11 (CUIL/CUIT) seguido de un máximo de 2 caracteres.')
            except Exception as e:
                print(f"Error Exeption en DNI/CUIL >> {str(e)}")
                raise forms.ValidationError(f'Ha ocurrido un error con el DNI/CUIL/CUIT ingresado.')
        if len(dni_str) > 13:
            raise forms.ValidationError("El DNI/CUIL/CUIT No debe contener mas de 13 caracteres alfanumericos.")

    def validate_document(self, data, model, type):
        """
        Metodo que uso para verificar si se creo una persona con un mismo DNI
        Recibimos como parametros:
        data >> Informacion del Documento De Identidad (DNI, CUIL)
        type >> Para saber el tipo de dato que estamos enviando sea un cuil o dni
        model >> Modelo o Objeto que estamos usando
        return raise ValidationError (Para mandar como un error de formulario.)
        """

        document = data
        if type == "DNI" or type == "dni":
            if model.objects.filter(dni=document).exists():
                raise forms.ValidationError(
                    f"Informacíon exístente en la BD. Modelo: {model._meta.model_name}"
                )
            return document
        elif type == "CUIL" or type == "cuil":
            if model.objects.filter(cuil=document).exists():
                raise forms.ValidationError(
                    f"Informacíon exístente en la BD. Modelo: {model._meta.model_name}"
                )
            return document