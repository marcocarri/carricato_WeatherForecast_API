from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone

from .models import DailyRequestTracker, SavedQuery
from .serializers import WeatherRequestSerializer, SavedQuerySerializer
from .utils import get_simulated_weather
from .permissions import IsPremiumUser


class WeatherForecastView(APIView):
    """
    endpoint per richiedere le previsioni meteo
    accessibile a tutti, ma limitato a 5 richieste al giorno per non-Premium.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. validazione input con il Serializer
        serializer = WeatherRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. controllo limite giornaliero
        if not (request.user.is_authenticated and getattr(request.user, 'is_premium', False)):
            today = timezone.now().date()

            # identifichiamo l'utente (se loggato) o l'IP (se anonimo)
            if request.user.is_authenticated:
                tracker, _ = DailyRequestTracker.objects.get_or_create(
                    user=request.user, date=today, defaults={'request_count': 0}
                )
            else:
                client_ip = request.META.get('REMOTE_ADDR')
                tracker, _ = DailyRequestTracker.objects.get_or_create(
                    ip_address=client_ip, date=today, user__isnull=True, defaults={'request_count': 0}
                )

            # se ha raggiunto il limite, lo blocchiamo
            if tracker.request_count >= 5:
                return Response(
                    {
                        "errore": "Limite giornaliero di 5 richieste raggiunto. Passa a Premium per richieste illimitate!"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            # altrimenti incrementiamo il contatore
            tracker.request_count += 1
            tracker.save()

        # 3. generazione Dati Meteo
        city = serializer.validated_data['city']
        target_date = serializer.validated_data['target_date']
        weather_data = get_simulated_weather(city, target_date)

        return Response(weather_data, status=status.HTTP_200_OK)


class SavedQueryViewSet(viewsets.ModelViewSet):
    """
    endpoint per gli utenti Premium: permette di salvare, listare e cancellare le query
    supporta GET (lista/singolo), POST (crea), DELETE (elimina).
    """
    serializer_class = SavedQuerySerializer
    permission_classes = [IsAuthenticated, IsPremiumUser]

    def get_queryset(self):
        # un utente vede solo le PROPRIE ricerche salvate
        return SavedQuery.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # quando l'utente salva una query, generiamo i dati meteo in background e li salviamo
        city = self.request.data.get('city')
        target_date = self.request.data.get('target_date')

        # validazione manuale extra pre-salvataggio
        if not city or not target_date:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"errore": "I campi 'city' e 'target_date' sono obbligatori per il salvataggio."})

        # otteniamo i dati meteo
        weather_data = get_simulated_weather(city, target_date)

        # salviamo associando l'utente loggato e i dati generati
        serializer.save(
            user=self.request.user,
            temperature=weather_data['temperature'],
            weather_condition=weather_data['weather_condition']
        )