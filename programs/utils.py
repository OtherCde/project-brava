from django.core.exceptions import ValidationError

# Definimos los días de la semana (recordá que Python usa 0=Lunes, 6=Domingo)
DAYS_OF_WEEK = {
    0: 'Lunes',
    1: 'Martes',
    2: 'Miércoles',
    3: 'Jueves',
    4: 'Viernes',
    5: 'Sábado',
    6: 'Domingo',
}

# Metodo que nos sirve para validar
def validation_program(object, program):
    new_start = object.start_time
    new_end = object.end_time

    # Se recorren los días en que se repite el programa
    for day in object.repeat_days:
        # Se filtran los programas que también se repiten en el mismo día,
        # excluyendo el mismo registro en caso de actualización.
        overlapping_programs = program.objects.filter(
            repeat_days__contains=[day]
        ).exclude(pk=object.pk)

        for program in overlapping_programs:
            existing_start = program.start_time
            existing_end = program.end_time

            # Verificamos si hay solapamiento:
            # Se considera solapamiento si:
            # 1. El nuevo programa comienza entre el inicio y fin de un existente.
            # 2. El nuevo programa finaliza entre el inicio y fin de un existente.
            # 3. El programa nuevo envuelve al existente.
            if ((existing_start <= new_start < existing_end) or
                (existing_start < new_end <= existing_end) or
                (new_start <= existing_start and new_end >= existing_end)):
                raise ValidationError(
                    f"Ya existe un programa el {DAYS_OF_WEEK[day]} "
                    f"de {existing_start.strftime('%H:%M')} a {existing_end.strftime('%H:%M')}, "
                    f"que se solapa con este horario."
                    )