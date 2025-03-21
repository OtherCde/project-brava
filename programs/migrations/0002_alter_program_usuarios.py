# Generated by Django 5.1.6 on 2025-02-17 17:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='usuarios',
            field=models.ManyToManyField(blank=True, help_text='Usuarios que participan en el programa (elenco)', null=True, related_name='programas', to=settings.AUTH_USER_MODEL),
        ),
    ]
