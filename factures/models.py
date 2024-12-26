from django.db import models
from vehicules.models import Vehicule
from utilisateurs.models import Client, Mecanicien
from rendez_vous.models import RendezVous  # Importez le modèle RendezVous

class Facture(models.Model):
    date = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="factures")
    mecanicien = models.ForeignKey(Mecanicien, on_delete=models.CASCADE, related_name="factures")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="factures" , default=1)  # Client associé
    rendezvous = models.OneToOneField(  # Une facture est associée à un seul rendez-vous
        RendezVous, 
        on_delete=models.CASCADE, 
        related_name="facture", default=1
    )
    def __str__(self):
        return f"Facture {self.id} - RendezVous: {self.rendezvous.id} - {self.date}"
