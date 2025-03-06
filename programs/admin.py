from django.contrib import admin
from .models import Program

# Register your models here.
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'category', 'get_host_name')
    list_filter = ('category', 'start_time', 'end_time')
    search_fields = ('title', 'description')
    ordering = ('start_time',)

admin.site.register(Program, ProgramAdmin)