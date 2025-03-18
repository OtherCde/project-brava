from django.contrib import admin
from django import forms
from .models import Program

# Definimos los días de la semana (recordá que en nuestro modelo 0 = Lunes, 6 = Domingo)
DAYS_OF_WEEK = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miércoles'),
    (3, 'Jueves'),
    (4, 'Viernes'),
    (5, 'Sábado'),
    (6, 'Domingo'),
)

class ProgramAdminForm(forms.ModelForm):
    # Usamos un MultipleChoiceField para seleccionar los días en los que se repite el programa
    repeat_days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text='Selecciona los días de la semana en los que se repite el programa.'
    )

    class Meta:
        model = Program
        fields = '__all__'

    def clean_repeat_days(self):
        # Convertimos los valores recibidos (como strings) a enteros
        data = self.cleaned_data.get('repeat_days', [])
        return list(map(int, data))

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Guardamos el campo repeat_days en el formato esperado (lista de enteros)
        instance.repeat_days = self.cleaned_data['repeat_days']
        if commit:
            instance.save()
        return instance

class ProgramAdmin(admin.ModelAdmin):
    form = ProgramAdminForm
    list_display = ('title', 'start_time', 'duration_in_minutes', 'category', 'get_host_name')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    ordering = ('title',)

admin.site.register(Program, ProgramAdmin)