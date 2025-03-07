from django.db import models

from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

# Create your models here.
class BaseAbstractWithUser(SoftDeletionModel, TimestampsModel):
    """
    Clase Abstracta para usar los modelos SoftDeletion y Timesstamps

    La clase incluye el created_at, updated_at, deleted_at y user_made
    """
    user_made = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Por", ## Referencia al usuario que esta manejando internamente el sistema
        related_name="%(class)s_user_made"
    ) # Es una RELACIÓM FOREINKEY ya que un USUARIO puede tener asociado multimples CAJAS, O MULTIPLES OBJETOS

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"Cambios realizados por: {self.user_made}"