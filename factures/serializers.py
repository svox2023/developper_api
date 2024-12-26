from rest_framework import serializers
from .models import Facture
from vehicules.models import Vehicule
from utilisateurs.models import Client, Mecanicien
from rendez_vous.models import RendezVous  # Importez le modèle RendezVous

class FactureSerializer(serializers.ModelSerializer):
    vehicule = serializers.StringRelatedField(read_only=True)  
    vehicule_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicule.objects.all(),
        write_only=True,
        source='vehicule',
        help_text="ID du véhicule lié à la facture",
        required=True
    )
    
    mecanicien = serializers.StringRelatedField(read_only=True)  
    mecanicien_id = serializers.PrimaryKeyRelatedField(
        queryset=Mecanicien.objects.all(),
        write_only=True,
        source='mecanicien',
        help_text="ID du mécanicien lié à la facture",
        required=True
    )
    
    client = serializers.StringRelatedField(read_only=True)  
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        write_only=True,
        source='client',
        help_text="ID du client associé à la facture",
        required=True
    )

    # Ajoutez le champ pour lier un rendez-vous
    rendezvous = serializers.StringRelatedField(read_only=True)  # Lecture seule pour afficher les détails
    rendezvous_id = serializers.PrimaryKeyRelatedField(
        queryset=RendezVous.objects.all(),
        write_only=True,
        source='rendezvous',  # Liez au champ `rendezvous` dans le modèle
        help_text="ID du rendez-vous associé à la facture",
        required=True
    )

    class Meta:
        model = Facture
        fields = [
            'id', 
            'date', 
            'montant', 
            'vehicule', 
            'vehicule_id', 
            'mecanicien', 
            'mecanicien_id',
            'client', 
            'client_id',
            'rendezvous',  # Affichage en lecture seule
            'rendezvous_id'  # Requis pour la création
        ]
        extra_kwargs = {
            'date': {'help_text': "Date de la facture au format AAAA-MM-JJ", 'required': True},
            'montant': {'help_text': "Montant de la facture", 'required': True},
        }

    def validate(self, data):
        """
        Validation personnalisée pour s'assurer que les données sont cohérentes.
        """
        if 'montant' in data and data['montant'] <= 0:
            raise serializers.ValidationError({"montant": "Le montant doit être supérieur à zéro."})
        return data
