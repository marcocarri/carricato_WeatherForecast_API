from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherForecastView, SavedQueryViewSet, WeatherStatsView

# il DefaultRouter gestisce automaticamente POST api/weather/saved per la richiesta+salvataggio e GET api/weather/saved per la visualizzazione della lista
router = DefaultRouter()
router.register(r'saved', SavedQueryViewSet, basename='saved-query')

urlpatterns = [
    # endpoint richiesta previsione meteo
    path('forecast/', WeatherForecastView.as_view(), name='weather-forecast'),
    # endpoint richiesta statistiche account
    path('stats/', WeatherStatsView.as_view(), name='weather-stats'),
    # endpoint(s) salvataggio richieste
    path('', include(router.urls)),
]