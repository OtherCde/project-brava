from django.db import models
from core.models import BaseAbstractWithUser


class Program(BaseAbstractWithUser):
    title = models.CharField(max_length=150)
    description = models.TextField(
        help_text="Una breve descripción sobre el programa"
    )
    start_time = models.DateTimeField(
        help_text="Fecha y hora de inicio del programa"
    )
    end_time = models.DateTimeField(
        help_text="Fecha y hora de fin del programa"
    )
    
    CATEGORY_CHOICES = [
        ('musica', 'Música'),
        ('deporte', 'Deporte'),
        ('noticias', 'Noticias'),
        ('cultura', 'Cultura'),
    ]
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        help_text="Categoría del programa"
    )
    image = models.ImageField(upload_to='program_images/', blank=True, null=True)

    # Host del programa (único por programa)
    host = models.OneToOneField(
        'users.User',
        on_delete=models.SET_NULL,
        related_name="hosted_program",
        null=True, blank=True,
        help_text="Encargado del programa"
    )

    # Participantes (elenco)
    usuarios = models.ManyToManyField(
        'users.User', 
        related_name="programas", 
        blank=True,
        help_text="Usuarios que participan en el programa (elenco)"
    )

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def get_host_name(self):
        """Devuelve el nombre del host del programa."""
        return self.host.get_full_name() if self.host else "Sin host asignado"

    def get_cast(self):
        """Devuelve una lista con los nombres de los usuarios participantes."""
        return [user.get_full_name() for user in self.usuarios.all()]
