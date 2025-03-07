from django.db import models
from django_timestamps.softDeletion import SoftDeletionManager
from django.contrib.auth.models import BaseUserManager

# Create here manangers
class UserManager(BaseUserManager, SoftDeletionManager):
    """
    Custom manager for User model with Soft Deletion and Timestamps
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un nuevo usuario con el email y la contraseña dados.
        """
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el email y la contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)