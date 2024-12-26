from rest_framework.authtoken.models import Token
from utilisateurs.models import Client, Mecanicien


def generate_tokens():
    # Générer des tokens pour tous les clients
    for client in Client.objects.all():
        token, created = Token.objects.get_or_create(user=client.user)
        print(f"Token généré pour le client {client.user.username}: {token.key}")

    # Générer des tokens pour tous les mécaniciens
    for mecanicien in Mecanicien.objects.all():
        token, created = Token.objects.get_or_create(user=mecanicien.user)
        print(f"Token généré pour le mécanicien {mecanicien.user.username}: {token.key}")
