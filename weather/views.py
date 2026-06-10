from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.db.models import Count, Avg

from .models import DailyRequestTracker, SavedQuery
from .serializers import WeatherRequestSerializer, SavedQuerySerializer
from .utils import get_simulated_weather
from .permissions import IsPremiumUser


class WeatherForecastView(APIView):
    """
    endpoint per richiedere le previsioni meteo
    accessibile a tutti, ma limitato a 5 richieste al giorno per non-Premium
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WeatherRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not (request.user.is_authenticated and getattr(request.user, 'is_premium', False)):
            today = timezone.now().date()

            if request.user.is_authenticated:
                tracker, _ = DailyRequestTracker.objects.get_or_create(
                    user=request.user, date=today, defaults={'request_count': 0}
                )
            else:
                client_ip = request.META.get('REMOTE_ADDR')
                tracker, _ = DailyRequestTracker.objects.get_or_create(
                    ip_address=client_ip, date=today, user__isnull=True, defaults={'request_count': 0}
                )

            if tracker.request_count >= 5:
                return Response(
                    {
                        "errore": "Limite giornaliero di 5 richieste raggiunto. Passa a Premium per richieste illimitate!"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            tracker.request_count += 1
            tracker.save()

        city = serializer.validated_data['city']
        target_date = serializer.validated_data['target_date']
        weather_data = get_simulated_weather(city, target_date)

        return Response(weather_data, status=status.HTTP_200_OK)


class SavedQueryViewSet(viewsets.ModelViewSet):
    """
    endpoint per gli utenti Premium: permette di salvare, listare e cancellare le query
    supporta GET (lista/singolo), POST (crea), DELETE (elimina)
    """
    serializer_class = SavedQuerySerializer
    permission_classes = [IsAuthenticated, IsPremiumUser]

    def get_queryset(self):
        return SavedQuery.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        city = self.request.data.get('city')
        target_date = self.request.data.get('target_date')

        if not city or not target_date:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"errore": "I campi 'city' e 'target_date' sono obbligatori per il salvataggio."})

        weather_data = get_simulated_weather(city, target_date)

        serializer.save(
            user=self.request.user,
            temperature=weather_data['temperature'],
            weather_condition=weather_data['weather_condition']
        )


class WeatherStatsView(APIView):
    """
    endpoint per le statistiche avanzate
    restituisce un'aggregazione dei dati storici dell'utente Premium
    """
    permission_classes = [IsAuthenticated, IsPremiumUser]

    def get(self, request):
        user_queries = SavedQuery.objects.filter(user=request.user)

        if not user_queries.exists():
            return Response({
                "messaggio": "Non hai ancora salvato nessuna ricerca meteo per generare le statistiche."
            }, status=status.HTTP_200_OK)

        total_queries = user_queries.count()

        avg_temp = user_queries.aggregate(Avg('temperature'))['temperature__avg']

        top_city_data = user_queries.values('city') \
                                    .annotate(search_count=Count('city')) \
                                    .order_by('-search_count') \
                                    .first()

        return Response({
            "totale_ricerche_salvate": total_queries,
            "temperatura_media_celsius": round(avg_temp, 1) if avg_temp else None,
            "citta_preferita": top_city_data['city'] if top_city_data else None,
            "volte_cercata": top_city_data['search_count'] if top_city_data else 0
        }, status=status.HTTP_200_OK)