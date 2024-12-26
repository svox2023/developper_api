from django.db import models
from utilisateurs.models import Client, Mecanicien
from vehicules.models import Vehicule

class RendezVous(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]

    date = models.DateTimeField()  # Date et heure du rendez-vous
    service = models.CharField(max_length=255)  # Type de service
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='en_attente',  # Par défaut, un rendez-vous est "En attente"
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="rendez_vous_client")
    mecanicien = models.ForeignKey(Mecanicien, on_delete=models.CASCADE, related_name="rendez_vous_mecanicien")
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="rendez_vous_vehicule")

    def __str__(self):
        return f"Rendez-vous {self.service} - {self.date} - Status: {self.get_status_display()}"
