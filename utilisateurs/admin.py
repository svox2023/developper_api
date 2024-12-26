from django.contrib import admin
from .models import Client, Mecanicien

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'get_username',
        'get_email',
        'get_first_name',
        'get_last_name',
        'birth_date',
        'get_mecanicien_username'
    )

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_mecanicien_username(self, obj):
        return obj.mecanicien.user.username if obj.mecanicien else "Aucun"
    get_mecanicien_username.short_description = "Mécanicien"


@admin.register(Mecanicien)
class MecanicienAdmin(admin.ModelAdmin):
    list_display = (
        'get_username',
        'get_email',
        'get_first_name',
        'get_last_name',
        'birth_date',
        'specialite',
        'disponibilite',
        'get_total_clients'
    )

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_total_clients(self, obj):
        return obj.clients.count()  # Accède au related_name "clients" dans le modèle Client
    get_total_clients.short_description = 'Nombre de clients'
