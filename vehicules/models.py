from django.db import models
from utilisateurs.models import Client
from django.db import models

class Vehicule(models.Model):
    vin = models.CharField(max_length=17, unique=True)  # Numéro d'identification du véhicule
    make = models.CharField(max_length=100)  # Marque 
    model = models.CharField(max_length=100)  # Modèle 
    year = models.PositiveIntegerField()  # Année de fabrication
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="vehicules")  

    def __str__(self):
        return f"Véhicule: {self.make} {self.model} ({self.year}) - VIN: {self.vin}"
