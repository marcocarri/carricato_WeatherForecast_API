from rest_framework import serializers
from .models import SavedQuery

class WeatherRequestSerializer(serializers.Serializer):
    """
    valida rigorosamente i parametri in ingresso per la query meteo
    """
    city = serializers.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'Il nome della città è obbligatorio.',
            'blank': 'Il nome della città non può essere vuoto.',
            'max_length': 'Il nome della città supera il limite di 100 caratteri.'
        }
    )
    target_date = serializers.DateField(
        required=True,
        error_messages={
            'required': 'La data (target_date) è obbligatoria.',
            'invalid': 'Formato data non valido. Usa il formato YYYY-MM-DD (es. 2026-07-12).'
        }
    )

    def validate_city(self, value):
        # ulteriore validazione custom: evitare numeri nel nome della città
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Il nome della città non può contenere numeri.")
        return value


class SavedQuerySerializer(serializers.ModelSerializer):
    """
    gestisce l'output e le operazioni CRUD per la cronologia dell'utente Premium.
    """
    class Meta:
        model = SavedQuery
        # escludiamo l'utente nei campi di input/output poiché verrà dedotto automaticamente dal token
        fields = ['id', 'city', 'target_date', 'temperature', 'weather_condition', 'saved_at']
        read_only_fields = ['id', 'temperature', 'weather_condition', 'saved_at']