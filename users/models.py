from django.contrib.auth.models import AbstractUser
from django.db import models

"""
modello Utente custom
gli utenti di base avranno is_premium=False, mentre gli utenti che 
acquistano/hanno il piano premium avranno is_premium=True
"""
class CustomUser(AbstractUser):

    is_premium = models.BooleanField(
        default=False,
        help_text="indica se l'utente ha privilegi Premium (richieste illimitate e salvataggio query)"
    )

    def __str__(self):
        role = "Premium" if self.is_premium else "Standard"
        return f"{self.username} ({role})"