# Generated by Django 5.1.6 on 2025-03-15 16:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0003_alter_program_usuarios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='end_time',
        ),
        migrations.AddField(
            model_name='program',
            name='duration_in_minutes',
            field=models.PositiveIntegerField(default=120, help_text='Duración del programa en minutos', validators=[django.core.validators.MinValueValidator(120)]),
        ),
        migrations.AddField(
            model_name='program',
            name='repeat_days',
            field=models.JSONField(default=list, help_text='Días de la semana en los que se repite el programa. (0=Lunes, 6=Domingo)'),
        ),
        migrations.AlterField(
            model_name='program',
            name='start_time',
            field=models.TimeField(help_text='Hora de inicio del programa'),
        ),
    ]
