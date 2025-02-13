from django.db import models
from django import forms
# Create your models here.
from django.contrib.auth.models import AbstractUser
from core.models import BaseAbstractWithUser

from .manangers import UserManager
from .utils import DEFAULT_PROFILE_IMAGE

from django.utils.translation import gettext_lazy as _

from django.conf import settings

class User(BaseAbstractWithUser, AbstractUser):

    profile_image = models.ImageField(
        upload_to="profile_images/",  # Guarda en media/profile_images/
        null=True,
        blank=True,
        verbose_name=_("Imagen de Perfil")
    )

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    objects = UserManager()  
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'users'
    
    def __str__(self):
        return self.username
    
    def get_string_for_is_active(self):
        if self.is_active:
            return "Usuarío activo."
        else:
            return "Usuarío inactivo."

    def get_full_name(self):
        return f"{self.first_name}, {self.last_name}"
    
    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return "/media/default.svg"

    def to_json(self):
        return {
            'id': self.id,
            'last_login': self.last_login,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'get_full_name': self.get_full_name(),
            'username': self.username,
            'email': self.email,
            'is_active': self.get_string_for_is_active(),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
            'is_staff': self.is_staff,
            'profile_image': self.get_profile_image_url(),  # Añadir la URL de la imagen
        }

        
