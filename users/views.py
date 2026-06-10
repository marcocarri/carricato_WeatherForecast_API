from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class UpgradePremiumView(APIView):
    """
    endpoint per simulare l'acquisto dell'abbonamento Premium
    richiede autenticazione (JWT)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.is_premium:
            return Response({"messaggio": "Sei già un utente Premium!"}, status=status.HTTP_400_BAD_REQUEST)

        # Effettuiamo l'upgrade!
        user.is_premium = True
        user.save()

        return Response({
            "messaggio": "Congratulazioni! Ora sei un utente Premium. Hai accesso alle ricerche meteo illimitate e al salvataggio dello storico."
        }, status=status.HTTP_200_OK)


class DowngradePremiumView(APIView):
    """
    endpoint per annullare l'abbonamento Premium e tornare Standard.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.is_premium:
            return Response({"messaggio": "Il tuo account è già Standard."}, status=status.HTTP_400_BAD_REQUEST)

        # Effettuiamo il downgrade
        user.is_premium = False
        user.save()

        return Response({
            "messaggio": "Hai disdetto l'abbonamento. Ora sei un utente Standard."
        }, status=status.HTTP_200_OK)