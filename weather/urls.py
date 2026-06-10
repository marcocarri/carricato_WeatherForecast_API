from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherForecastView, SavedQueryViewSet, WeatherStatsView

# il DefaultRouter gestisce automaticamente tutti gli URL per le operazioni CRUD del ViewSet
router = DefaultRouter()
router.register(r'saved', SavedQueryViewSet, basename='saved-query')

urlpatterns = [
    path('forecast/', WeatherForecastView.as_view(), name='weather-forecast'),
    path('stats/', WeatherStatsView.as_view(), name='weather-stats'),
    path('', include(router.urls)),
]