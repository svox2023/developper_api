from rest_framework import serializers
from .models import Vehicule
from utilisateurs.models import Client


class VehiculeSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Vehicule.
    """
    client = serializers.StringRelatedField(read_only=True)  # Affichage des informations du client en lecture seule
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        write_only=True,
        source="client",  # Permet de lier automatiquement à l'objet `Client`
        help_text="ID du client associé au véhicule"
    )

    class Meta:
        model = Vehicule
        fields = ['id', 'vin', 'make', 'model', 'year', 'client', 'client_id']

    def create(self, validated_data):
        """
        Création d'un véhicule avec l'ID client fourni.
        """
        return Vehicule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Mise à jour des informations d'un véhicule.
        """
        # Mise à jour des champs fournis
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
