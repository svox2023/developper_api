from rest_framework import serializers
from .models import RendezVous
from utilisateurs.models import Client, Mecanicien
from vehicules.models import Vehicule

class RendezVousSerializer(serializers.ModelSerializer):
    # Champs de lecture seule
    client = serializers.StringRelatedField(read_only=True)  # Affiche les informations lisibles du client
    mecanicien = serializers.StringRelatedField(read_only=True)  # Affiche les informations lisibles du mécanicien
    vehicule = serializers.StringRelatedField(read_only=True)  # Affiche les informations lisibles du véhicule

    # Champs pour recevoir les IDs en écriture
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        write_only=True,
        source="client",
        help_text="ID du client associé au rendez-vous",
        required=True
    )
    mecanicien_id = serializers.PrimaryKeyRelatedField(
        queryset=Mecanicien.objects.all(),
        write_only=True,
        source="mecanicien",
        help_text="ID du mécanicien responsable du rendez-vous",
        required=True
    )
    vehicule_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicule.objects.all(),
        write_only=True,
        source="vehicule",
        help_text="ID du véhicule concerné par le rendez-vous",
        required=True
    )

    # Champ status avec documentation et validation
    status = serializers.ChoiceField(
        choices=RendezVous.STATUS_CHOICES,
        default='en_attente',
        help_text="Statut du rendez-vous ('en_attente', 'confirme', 'annule', 'termine')"
    )

    class Meta:
        model = RendezVous
        fields = [
            'id',
            'date',
            'service',
            'status',
            'client',  # Lecture seule
            'mecanicien',  # Lecture seule
            'vehicule',  # Lecture seule
            'client_id',  # Écriture uniquement
            'mecanicien_id',  # Écriture uniquement
            'vehicule_id'  # Écriture uniquement
        ]
        extra_kwargs = {
            'date': {'help_text': "Date et heure du rendez-vous au format ISO (AAAA-MM-JJ HH:MM:SS)", 'required': True},
            'service': {'help_text': "Description du service demandé (exemple : Révision, Changement de pneus)", 'required': True},
        }

    def validate(self, data):
        """
        Validation personnalisée pour garantir la cohérence des données.
        """
        if 'status' in data and data['status'] not in [choice[0] for choice in RendezVous.STATUS_CHOICES]:
            raise serializers.ValidationError({"status": "Statut invalide. Choisissez parmi : 'en_attente', 'confirme', 'annule', 'termine'."})
        return data
