from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User  # Importa tu modelo de usuario personalizado

import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def asignar_grupo_por_defecto(sender, instance, created, **kwargs):
    if created:  # Solo se ejecuta cuando el usuario es nuevo
        grupo_oyentes = Group.objects.get(name="Oyentes")
        instance.groups.add(grupo_oyentes)
        logger.info(f"Se asignó el grupo 'Oyentes' al usuario {instance.username}")
