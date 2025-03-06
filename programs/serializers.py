from rest_framework import serializers
from .models import Program

class ProgramSerializer(serializers.ModelSerializer):
    host_name = serializers.SerializerMethodField()
    cast = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            'id', 'title', 'description', 'start_time', 'end_time',
            'category', 'image', 'host_name', 'cast'
        ]

    def get_host_name(self, obj):
        """Devuelve el nombre del host si existe."""
        return obj.host.get_full_name() if obj.host else "Sin host asignado"

    def get_cast(self, obj):
        """Devuelve la lista de nombres de los usuarios participantes."""
        return [user.get_full_name() for user in obj.usuarios.all()]