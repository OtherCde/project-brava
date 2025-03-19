from django.contrib import admin
from .models import Advertisement

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'status', 'user_made', 'created_at')  # Muestra estos campos en la lista
    list_filter = ('status', 'created_at')  # Agrega filtros por estado y fecha de creación
    search_fields = ('company_name', 'link')  # Permite búsqueda por nombre y enlace
    ordering = ('-created_at',)  # Ordena por fecha de creación descendente
    readonly_fields = ('created_at', 'updated_at', 'user_made')  # Campos de solo lectura

    fieldsets = (
        (None, {
            'fields': ('company_name', 'image', 'link', 'status')
        }),
        ("Metadata", {
            'fields': ('user_made', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Asigna automáticamente el usuario que crea el anuncio."""
        if not obj.pk:  # Solo establece user_made en la creación, no en edición
            obj.user_made = request.user
        super().save_model(request, obj, form, change)
