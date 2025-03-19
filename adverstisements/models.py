from django.db import models
from core.models import BaseAbstractWithUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Advertisement(BaseAbstractWithUser):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    company_name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='advertisements/', 
        null=True, 
        blank=True, 
        verbose_name=_("imagen_publicitario")
    )
    link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.company_name