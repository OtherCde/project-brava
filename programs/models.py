from django.db import models
from core.models import BaseAbstractWithUser
from datetime import date, datetime, timedelta
from django.core.validators import MinValueValidator

# Definimos los días de la semana (recordá que Python usa 0=Lunes, 6=Domingo)
DAYS_OF_WEEK = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miércoles'),
    (3, 'Jueves'),
    (4, 'Viernes'),
    (5, 'Sábado'),
    (6, 'Domingo'),
)

class Program(BaseAbstractWithUser):
    title = models.CharField(max_length=150)
    description = models.TextField(
        help_text="Una breve descripción sobre el programa"
    )
    
    # Hora de inicio del programa (solo la hora)
    start_time = models.TimeField(help_text="Hora de inicio del programa")
    
    # Duración del programa en minutos (por ejemplo, 120 para dos horas)
    duration_in_minutes = models.PositiveIntegerField(
        help_text="Duración del programa en minutos",
        default=120,
        validators=[MinValueValidator(120)]
    )
    
    # Campo para almacenar los días en que se repite el programa.
    # Se puede almacenar como una lista de números, ej.: [0,2,4] para lunes, miércoles y viernes.
    repeat_days = models.JSONField(
        help_text="Días de la semana en los que se repite el programa. (0=Lunes, 6=Domingo)",
        default=list
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

    # La hora de fin se puede calcular a partir de start_time y duration.
    @property
    def end_time(self):
        # Se calcula combinando la fecha actual con la hora de inicio y sumándole la duración.
        # Esto es solo un ejemplo para obtener la hora (sin considerar fechas).
        today = date.today()
        start_dt = datetime.combine(today, self.start_time)
        end_dt = start_dt + timedelta(minutes=self.duration_in_minutes)
        return end_dt.time()

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def get_host_name(self):
        """Devuelve el nombre del host del programa."""
        return self.host.get_full_name() if self.host else "Sin host asignado"

    def get_cast(self):
        """Devuelve una lista con los nombres de los usuarios participantes."""
        return [user.get_full_name() for user in self.usuarios.all()]
