from rest_framework.permissions import BasePermission

class IsPremiumUser(BasePermission):
    """
    permette l'accesso solo agli utenti autenticati che hanno is_premium = True
    """
    message = "Accesso negato. Questa funzionalità è riservata agli utenti Premium."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_premium', False))