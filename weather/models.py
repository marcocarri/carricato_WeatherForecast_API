from django.db import models
from django.conf import settings
from django.utils import timezone

"""
traccia il numero di richieste meteo effettuate in una specifica giornata
se l'utente è autenticato, usiamo la ForeignKey `user`, mentre, se è anonimo, tracciamo tramite `ip_address`
"""
class DailyRequestTracker(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='daily_requests'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    date = models.DateField(default=timezone.now)
    request_count = models.IntegerField(default=1)

    class Meta:
        # verifichiamo che ci sia un solo record per (utente, data) (utente autenticato) o (ip, data) (utente anonimo)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'],
                name='unique_user_daily_request',
                condition=models.Q(user__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['ip_address', 'date'],
                name='unique_ip_daily_request',
                condition=models.Q(user__isnull=True)
            )
        ]

    def __str__(self):
        identifier = self.user.username if self.user else self.ip_address
        return f"{identifier} - {self.date} - Richieste: {self.request_count}"

"""
memorizza le ricerche meteo salvate dagli utenti Premium, (relazione ForeignKey con CustomUser)
"""
class SavedQuery(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_queries'
    )
    city = models.CharField(max_length=100)
    target_date = models.DateField(help_text="Data per cui è stata richiesta la previsione")
    # salviamo uno snapshot dei risultati per lo storico
    temperature = models.FloatField(help_text="Temperatura in gradi Celsius")
    weather_condition = models.CharField(max_length=100, help_text="Es. Soleggiato, Pioggia, Nuvoloso")

    # metadati
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']

    def __str__(self):
        return f"Query di {self.user.username} per {self.city} del {self.target_date}"