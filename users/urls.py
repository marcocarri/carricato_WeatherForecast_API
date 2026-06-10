from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UpgradePremiumView, DowngradePremiumView, UserAdminViewSet

# il DefaultRouter gestisce automaticamente /api/users/manage/ per la lista e /api/users/manage/<id>/ per le singole operazioni
router = DefaultRouter()
router.register(r'manage', UserAdminViewSet, basename='admin-manage-users')

urlpatterns = [
    # endpoint login (crea il JWT)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # endpoint refresh (rinnova il JWT)
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # endpoint registrazione
    path('register/', RegisterView.as_view(), name='register'),
    # endpoint upgrade account
    path('upgrade/', UpgradePremiumView.as_view(), name='upgrade_premium'),
    # endpoint downgrade account
    path('downgrade/', DowngradePremiumView.as_view(), name='downgrade_premium'),
    # endpoint(s) dell'amministratore
    path('', include(router.urls)),
]