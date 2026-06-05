from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# estendiamo i campi mostrati nel pannello admin per includere 'is_premium'
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Ruoli Personalizzati', {'fields': ('is_premium',)}),
    )

# registriamo il modello CustomUser nel pannello Admin
admin.site.register(CustomUser, CustomUserAdmin)