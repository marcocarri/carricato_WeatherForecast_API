from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    # endpoint login (crea il JWT)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # endpoint refresh (rinnova il JWT)
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # endpoint registrazione
    path('register/', RegisterView.as_view(), name='register'),
]